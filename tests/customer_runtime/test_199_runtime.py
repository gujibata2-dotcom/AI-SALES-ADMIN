import os, tempfile, unittest
from pathlib import Path
from app.api.customer_runtime.runtime import Store, Auth, CustomerRuntime, AuthorizationError, ModelNotConfigured

class Runtime199Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.NamedTemporaryFile(delete=False); self.tmp.close()
        self.store=Store(Path(self.tmp.name)); self.auth=Auth(self.store); self.rt=CustomerRuntime(self.store)
    def tearDown(self): os.unlink(self.tmp.name)
    def test_register_login_tenant(self):
        uid,tid=self.auth.register('a@example.test','strong-password-123'); token=self.auth.login('a@example.test','strong-password-123'); ctx=self.auth.context(token); self.assertEqual(ctx.tenant_id,tid); self.assertEqual(ctx.user_id,uid)
    def test_199_entitlement_and_employee_limit(self):
        _,tid=self.auth.register('b@example.test','strong-password-123'); self.rt.activate_199(tid,'sub_test'); ctx=self.auth.context(self.auth.login('b@example.test','strong-password-123'))
        self.rt.create_employee(ctx,'Sales AI','Sales','sell honestly'); self.rt.create_employee(ctx,'Support AI','Support','resolve customer issues')
        with self.assertRaises(AuthorizationError): self.rt.create_employee(ctx,'Third','Admin','x')
    def test_cross_tenant_employee_blocked(self):
        _,t1=self.auth.register('c@example.test','strong-password-123'); _,t2=self.auth.register('d@example.test','strong-password-123'); self.rt.activate_199(t1,'s1'); self.rt.activate_199(t2,'s2')
        c1=self.auth.context(self.auth.login('c@example.test','strong-password-123')); c2=self.auth.context(self.auth.login('d@example.test','strong-password-123')); eid=self.rt.create_employee(c1,'A','Sales','x')
        with self.assertRaises(AuthorizationError): self.rt.execute_task(c2,eid,'hello','idem-cross')
    def test_idempotency_before_model(self):
        _,tid=self.auth.register('e@example.test','strong-password-123'); self.rt.activate_199(tid,'s3'); ctx=self.auth.context(self.auth.login('e@example.test','strong-password-123')); eid=self.rt.create_employee(ctx,'A','Sales','x')
        with self.assertRaises(ModelNotConfigured): self.rt.execute_task(ctx,eid,'hello','same-key')
        # The failed attempt is not retried blindly; a real provider is required.
        with self.assertRaises(ModelNotConfigured): self.rt.execute_task(ctx,eid,'hello','same-key-2')

if __name__=='__main__': unittest.main()
