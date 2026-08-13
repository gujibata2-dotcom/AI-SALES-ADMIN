from __future__ import annotations
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .runtime import Auth, CustomerRuntime, StripeAdapter, AuthorizationError, PaymentNotConfigured, ModelNotConfigured

store = CustomerRuntime().store
runtime = CustomerRuntime(store)
auth = Auth(store)
stripe = StripeAdapter()

def body(handler):
    n=int(handler.headers.get('Content-Length','0')); return json.loads(handler.rfile.read(n) or b'{}')

class Handler(BaseHTTPRequestHandler):
    def send_json(self,status,payload):
        raw=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/health': return self.send_json(200,{'status':'ok','service':'customer-runtime'})
        self.send_json(404,{'error':'NOT_FOUND'})
    def do_POST(self):
        try:
            data=body(self)
            if self.path=='/v1/auth/register':
                uid,tid=auth.register(data['email'],data['password']); return self.send_json(201,{'user_id':uid,'tenant_id':tid})
            if self.path=='/v1/auth/login': return self.send_json(200,{'token':auth.login(data['email'],data['password'])})
            if self.path=='/v1/billing/checkout/199':
                ctx=auth.context(self.headers.get('Authorization','').removeprefix('Bearer ')); session=stripe.checkout_url(ctx.tenant_id,data['success_url'],data['cancel_url']); return self.send_json(200,{'checkout_url':session.get('url'),'session_id':session.get('id')})
            if self.path=='/v1/billing/webhook':
                raw=json.dumps(data,separators=(',',':')).encode(); stripe.verify_signature(raw,self.headers.get('Stripe-Signature','')); event_type=data.get('type',''); obj=data.get('data',{}).get('object',{}); tenant_id=obj.get('client_reference_id') or obj.get('metadata',{}).get('tenant_id');
                if event_type in ('checkout.session.completed','customer.subscription.created','customer.subscription.updated') and tenant_id: runtime.activate_199(tenant_id,obj.get('id','unknown'))
                return self.send_json(200,{'received':True})
            token=self.headers.get('Authorization','').removeprefix('Bearer '); ctx=auth.context(token)
            if self.path=='/v1/employees':
                eid=runtime.create_employee(ctx,data['name'],data['role'],data.get('objective',''),data.get('knowledge',''),data.get('permissions')); return self.send_json(201,{'employee_id':eid})
            if self.path=='/v1/tasks':
                result=runtime.execute_task(ctx,data['employee_id'],data['prompt'],data['idempotency_key']); return self.send_json(200,result)
            self.send_json(404,{'error':'NOT_FOUND'})
        except (AuthorizationError,PaymentNotConfigured,ModelNotConfigured,ValueError) as exc:
            self.send_json(403 if isinstance(exc,AuthorizationError) else 400,{'error':str(exc)})
        except Exception as exc:
            self.send_json(500,{'error':'INTERNAL_ERROR','type':type(exc).__name__})
    def log_message(self,*args): pass

if __name__=='__main__':
    ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8080'))),Handler).serve_forever()
