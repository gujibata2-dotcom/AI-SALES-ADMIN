from __future__ import annotations
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .runtime import Auth, CustomerRuntime, StripeAdapter, AuthorizationError, PaymentNotConfigured, ModelNotConfigured, PaymentVerificationError

store = CustomerRuntime().store
runtime = CustomerRuntime(store)
auth = Auth(store)
stripe = StripeAdapter()

def json_body(handler):
    n=int(handler.headers.get('Content-Length','0')); return json.loads(handler.rfile.read(n) or b'{}')

class Handler(BaseHTTPRequestHandler):
    def send_json(self,status,payload):
        raw=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/health': return self.send_json(200,{'status':'ok','service':'customer-runtime'})
        self.send_json(404,{'error':'NOT_FOUND'})
    def do_POST(self):
        try:
            if self.path=='/v1/billing/webhook':
                n=int(self.headers.get('Content-Length','0')); raw=self.rfile.read(n); stripe.verify_signature(raw,self.headers.get('Stripe-Signature','')); data=json.loads(raw or b'{}')
                event_id=data.get('id')
                if not event_id: raise PaymentVerificationError('EVENT_ID_MISSING')
                event_type=data.get('type',''); obj=data.get('data',{}).get('object',{})
                if event_type=='checkout.session.completed':
                    tenant_id=obj.get('client_reference_id') or obj.get('metadata',{}).get('tenant_id')
                    if not tenant_id: raise PaymentVerificationError('TENANT_REFERENCE_MISSING')
                    session=stripe.retrieve_session(obj.get('id',''))
                    runtime.activate_199(tenant_id,obj.get('id',''),event_id,session)
                elif event_type in ('charge.refunded','charge.dispute.created'):
                    payment_ref=obj.get('payment_intent') or obj.get('id')
                    row=store.db.execute('SELECT tenant_id FROM billing_transactions WHERE payment_reference=?',(payment_ref,)).fetchone()
                    if row:
                        status='PAYMENT_REFUNDED' if event_type=='charge.refunded' else 'PAYMENT_DISPUTED'
                        store.db.execute('UPDATE billing_transactions SET status=?,updated_at=? WHERE payment_reference=?',(status,__import__('time').time(),payment_ref))
                        store.db.execute("UPDATE subscriptions SET status='CANCELED' WHERE tenant_id=? AND plan_id='199' AND status='ACTIVE'",(row['tenant_id'],)); store.db.commit(); store.audit(row['tenant_id'],'stripe',status,{'payment_reference':payment_ref,'event_id':event_id})
                return self.send_json(200,{'received':True})
            data=json_body(self)
            if self.path=='/v1/auth/register':
                uid,tid=auth.register(data['email'],data['password']); return self.send_json(201,{'user_id':uid,'tenant_id':tid})
            if self.path=='/v1/auth/login': return self.send_json(200,{'token':auth.login(data['email'],data['password'])})
            token=self.headers.get('Authorization','').removeprefix('Bearer '); ctx=auth.context(token)
            if self.path=='/v1/billing/checkout/199':
                session=stripe.checkout_url(ctx.tenant_id,data['success_url'],data['cancel_url']); return self.send_json(200,{'checkout_url':session.get('url'),'session_id':session.get('id')})
            if self.path=='/v1/employees':
                eid=runtime.create_employee(ctx,data['name'],data['role'],data.get('objective',''),data.get('knowledge',''),data.get('permissions')); return self.send_json(201,{'employee_id':eid})
            if self.path=='/v1/tasks':
                result=runtime.execute_task(ctx,data['employee_id'],data['prompt'],data['idempotency_key']); return self.send_json(200,result)
            self.send_json(404,{'error':'NOT_FOUND'})
        except (AuthorizationError,PaymentNotConfigured,ModelNotConfigured,PaymentVerificationError,ValueError) as exc:
            self.send_json(403 if isinstance(exc,AuthorizationError) else 400,{'error':str(exc)})
        except Exception as exc:
            self.send_json(500,{'error':'INTERNAL_ERROR','type':type(exc).__name__})
    def log_message(self,*args): pass

if __name__=='__main__':
    ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8080'))),Handler).serve_forever()
