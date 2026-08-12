"""Phase 25 reliability, observability and bounded self-healing control plane.
No external side effects. Recovery is policy/authorization driven and never changes governance or privileges.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class HealthStatus(str, Enum): HEALTHY="HEALTHY"; DEGRADED="DEGRADED"; UNHEALTHY="UNHEALTHY"; UNKNOWN="UNKNOWN"; OFFLINE="OFFLINE"
class IncidentSeverity(str, Enum): INFO="INFO"; WARNING="WARNING"; HIGH="HIGH"; CRITICAL="CRITICAL"
class IncidentStatus(str, Enum): OPEN="OPEN"; INVESTIGATING="INVESTIGATING"; MITIGATING="MITIGATING"; RECOVERED="RECOVERED"; RESOLVED="RESOLVED"; CLOSED="CLOSED"
class EvidenceKind(str, Enum): OBSERVED="OBSERVED"; INFERRED="INFERRED"; UNKNOWN="UNKNOWN"
class DiagnosisConfidence(str, Enum): HIGH="HIGH"; MEDIUM="MEDIUM"; LOW="LOW"
class CircuitState(str, Enum): CLOSED="CLOSED"; OPEN="OPEN"; HALF_OPEN="HALF_OPEN"
class RecoveryStatus(str, Enum): PLANNED="PLANNED"; AUTHORIZED="AUTHORIZED"; RUNNING="RUNNING"; VERIFIED="VERIFIED"; FAILED="FAILED"; ESCALATED="ESCALATED"; STOPPED="STOPPED"

@dataclass(frozen=True)
class HealthCheck:
    name: str; passed: bool; evidence: Any=None; warning: str|None=None
@dataclass(frozen=True)
class HealthReport:
    health_id: str; component_id: str; component_type: str; status: HealthStatus; health_score: float|None
    checks: tuple[HealthCheck,...]; warnings: tuple[str,...]=(); incidents: tuple[str,...]=(); last_checked: str=""; next_check: str=""
@dataclass(frozen=True)
class TelemetryEvent:
    event_type: str; timestamp: str; employee_id: str|None=None; team_id: str|None=None; workflow_id: str|None=None
    task_id: str|None=None; execution_id: str|None=None; incident_id: str|None=None; attributes: dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class Incident:
    incident_id: str; severity: IncidentSeverity; source: str; affected_components: tuple[str,...]; description: str
    detected_at: str; status: IncidentStatus=IncidentStatus.OPEN; root_cause: str|None=None; impact: dict[str,Any]=field(default_factory=dict)
    recovery_plan: str|None=None; resolution: str|None=None; owner: str|None=None; timeline: tuple[str,...]=()
@dataclass(frozen=True)
class Diagnosis:
    category: str; evidence_kind: EvidenceKind; confidence: DiagnosisConfidence; explanation: str
@dataclass(frozen=True)
class RecoveryPolicy:
    allowed_actions: tuple[str,...]; max_attempts: int; timeout_seconds: int; backoff_seconds: int; scope: tuple[str,...]
    destructive: bool=False
@dataclass
class RecoveryResult:
    status: RecoveryStatus; incident_id: str; action: str; actor: str; authorization: str; policy: str
    reason: str; result: Any=None; verification: Any=None; attempts: int=0; timestamp: str=""

class HealthEngine:
    @staticmethod
    def evaluate(component_id, component_type, checks, now="", next_check="") -> HealthReport:
        checks=tuple(checks)
        if not checks or any(c.evidence is None for c in checks): status=HealthStatus.UNKNOWN; score=None
        else:
            passed=sum(c.passed for c in checks)/len(checks); score=passed
            status=HealthStatus.HEALTHY if passed==1 else HealthStatus.DEGRADED if passed>0 else HealthStatus.UNHEALTHY
        return HealthReport(f"health:{component_id}",component_id,component_type,status,score,checks,last_checked=now,next_check=next_check)

class AlertCorrelator:
    def __init__(self): self._groups={}
    def fingerprint(self, source, component, signature): return f"{source}:{component}:{signature}"
    def correlate(self, source, component, signature, incident_id):
        fp=self.fingerprint(source,component,signature); self._groups.setdefault(fp,incident_id); return self._groups[fp]

class DiagnosisEngine:
    @staticmethod
    def classify(observed: bool, explanation: str|None, confidence: DiagnosisConfidence) -> Diagnosis:
        if not observed: return Diagnosis("unknown",EvidenceKind.UNKNOWN,DiagnosisConfidence.LOW,"insufficient evidence")
        return Diagnosis("unknown",EvidenceKind.INFERRED if explanation else EvidenceKind.OBSERVED,confidence,explanation or "observed condition")

class CircuitBreaker:
    def __init__(self, failure_threshold:int=5): self.failure_threshold=failure_threshold; self.failures=0; self.state=CircuitState.CLOSED
    def failure(self):
        self.failures+=1
        if self.failures>=self.failure_threshold: self.state=CircuitState.OPEN
    def half_open(self):
        if self.state is CircuitState.OPEN: self.state=CircuitState.HALF_OPEN
    def success(self): self.failures=0; self.state=CircuitState.CLOSED

class RecoveryEngine:
    FORBIDDEN={"financial_failure","legal_action","security_incident","privacy_breach","irreversible_action","unknown_critical_failure"}
    def recover(self, incident: Incident, diagnosis: Diagnosis, policy: RecoveryPolicy, action: str, *, authorized: bool, kill_switch: bool=False) -> RecoveryResult:
        if kill_switch: return RecoveryResult(RecoveryStatus.STOPPED,incident.incident_id,action,"system","kill-switch","external-governance","kill switch active")
        if incident.severity is IncidentSeverity.CRITICAL and diagnosis.category in self.FORBIDDEN:
            return RecoveryResult(RecoveryStatus.ESCALATED,incident.incident_id,action,"system","none","governance","human/security escalation required")
        if not authorized or action not in policy.allowed_actions or policy.max_attempts<=0 or policy.destructive:
            return RecoveryResult(RecoveryStatus.STOPPED,incident.incident_id,action,"system","denied","policy","recovery blocked")
        return RecoveryResult(RecoveryStatus.AUTHORIZED,incident.incident_id,action,"system","approved","policy","safe recovery authorized")

class RunawayDetector:
    def check(self, tasks:int, parallel:int, retries:int, duration:int, cost:float, delegation:int, limits:dict) -> str|None:
        checks=(("max_tasks",tasks),("max_parallel",parallel),("max_retries",retries),("max_duration",duration),("max_cost",cost),("max_delegation_depth",delegation))
        for key,value in checks:
            if key in limits and value>limits[key]: return key
        return None

class DeadLetterQueue:
    def __init__(self): self.items=[]
    def put(self, context, error, audit): self.items.append({"context":context,"error":error,"audit":audit})

class KillSwitch:
    def __init__(self): self.stopped=set()
    def stop(self, scope): self.stopped.add(scope)
    def is_stopped(self, scope): return scope in self.stopped
    def resume(self, scope): self.stopped.discard(scope)

class ReliabilityGuard:
    """AI cannot disable monitoring, kill switches, audit, governance, or security controls."""
    FORBIDDEN={"disable_monitoring","disable_kill_switch","modify_incident_severity","hide_failure","delete_audit","change_governance","bypass_recovery_authorization"}
    def allow(self, action): return action not in self.FORBIDDEN
