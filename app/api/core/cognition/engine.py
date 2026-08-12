from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class Outcome(str, Enum): SUCCESS='SUCCESS'; PARTIAL_SUCCESS='PARTIAL_SUCCESS'; FAILURE='FAILURE'; UNKNOWN='UNKNOWN'
class KnowledgeStatus(str, Enum): UNVERIFIED='UNVERIFIED'; PENDING_REVIEW='PENDING_REVIEW'; VERIFIED='VERIFIED'; CONFLICTED='CONFLICTED'; EXPIRED='EXPIRED'; REJECTED='REJECTED'
class Certainty(str, Enum): KNOWN='KNOWN'; PROBABLY_KNOWN='PROBABLY_KNOWN'; UNCERTAIN='UNCERTAIN'; UNKNOWN='UNKNOWN'

@dataclass(frozen=True)
class AttentionItem:
    item_id:str; relevance:float; importance:float; priority:float; expires_at:float|None=None
    @property
    def score(self): return self.relevance * self.importance * self.priority

class AttentionEngine:
    def select(self, task:str, goal:str, candidates:list[AttentionItem], limit:int=20):
        return sorted(candidates, key=lambda x:x.score, reverse=True)[:max(0,limit)]

@dataclass
class WorkingMemory:
    max_items:int=32; items:list[Mapping[str,Any]]=field(default_factory=list)
    def put(self,item):
        self.items.append(dict(item)); self.items=self.items[-self.max_items:]
    def clear_expired(self, now:float):
        self.items=[x for x in self.items if x.get('expires_at') is None or x['expires_at']>now]

@dataclass(frozen=True)
class Episode:
    episode_id:str; employee_id:str; task_id:str; timestamp:str; context:Mapping[str,Any]; action:Mapping[str,Any]; result:Mapping[str,Any]; feedback:Mapping[str,Any]|None; error:Mapping[str,Any]|None; correction:Mapping[str,Any]|None; outcome:Outcome; confidence:float

@dataclass(frozen=True)
class KnowledgeItem:
    knowledge_id:str; kind:str; content:Mapping[str,Any]; source:str; confidence:float; verification_status:KnowledgeStatus; created_at:str; updated_at:str; expiration:str|None=None; version:int=1

@dataclass(frozen=True)
class Procedure:
    procedure_id:str; trigger:str; steps:tuple[str,...]; decision_points:tuple[str,...]; expected_outcome:str; failure_conditions:tuple[str,...]

@dataclass(frozen=True)
class Experience:
    experience_id:str; task_id:str; outcome:Outcome; context:Mapping[str,Any]; decision:Mapping[str,Any]; feedback:Mapping[str,Any]|None; evidence:tuple[str,...]=()

@dataclass(frozen=True)
class ErrorAnalysis:
    error_id:str; context:Mapping[str,Any]; cause_status:Certainty; cause:str; failed_assumption:str|None; missing_information:tuple[str,...]; action:str; correction:str; prevention_rule:str|None

@dataclass(frozen=True)
class Reflection:
    reflection_id:str; goal:str; actions:tuple[str,...]; observed:str; worked:tuple[str,...]; failed:tuple[str,...]; uncertain:tuple[str,...]; learned:tuple[str,...]; changes:tuple[str,...]

class SelfEvaluator:
    def evaluate(self, accuracy:float, reasoning_quality:float, task_success:float, efficiency:float, policy_compliance:float, customer_outcome:float, confidence:float):
        return {'accuracy':accuracy,'reasoning_quality':reasoning_quality,'task_success':task_success,'efficiency':efficiency,'policy_compliance':policy_compliance,'customer_outcome':customer_outcome,'confidence':confidence,'certainty':self.calibrate(confidence,accuracy)}
    def calibrate(self, confidence, accuracy):
        if confidence>0.8 and accuracy<0.6: return Certainty.UNCERTAIN.value
        if accuracy>=0.9: return Certainty.KNOWN.value
        if accuracy>=0.7: return Certainty.PROBABLY_KNOWN.value
        if accuracy==0: return Certainty.UNKNOWN.value
        return Certainty.UNCERTAIN.value

@dataclass(frozen=True)
class KnowledgeGap:
    gap_id:str; topic:str; reason:str; severity:str; frequency:int; impact:float; confidence:float

class GapDetector:
    def detect(self, topic, reason, severity='MEDIUM', frequency=1, impact=0.5, confidence=0.0):
        return KnowledgeGap(f'gap:{topic}',topic,reason,severity,frequency,impact,confidence)

@dataclass(frozen=True)
class ResearchResult:
    research_id:str; gap_id:str; sources:tuple[Mapping[str,Any],...]; evidence:tuple[str,...]; verification_status:KnowledgeStatus; conflicts:tuple[str,...]=()

class SourceVerifier:
    RANK={'PRIMARY':4,'OFFICIAL':4,'RELIABLE_SECONDARY':3,'COMMUNITY':2,'UNKNOWN':0}
    def verify(self, sources):
        if not sources: return KnowledgeStatus.UNVERIFIED
        if any(self.RANK.get(s.get('quality','UNKNOWN'),0)>=4 for s in sources): return KnowledgeStatus.VERIFIED
        if len(sources)>=2 and len({s.get('claim') for s in sources})==1: return KnowledgeStatus.VERIFIED
        return KnowledgeStatus.PENDING_REVIEW

@dataclass(frozen=True)
class LearningCandidate:
    candidate_id:str; change_type:str; evidence:tuple[str,...]; conditions:Mapping[str,Any]; confidence:float; risk:str; approval_required:bool=True

class LearningGate:
    def approve(self,candidate:LearningCandidate, governance_approved:bool, evaluation_passed:bool):
        return governance_approved and evaluation_passed and candidate.approval_required

class GoalPersistence:
    def __init__(self, authorized_goal:str): self.authorized_goal=authorized_goal
    def check(self, goal:str): return goal==self.authorized_goal

@dataclass
class Skill:
    skill_id:str; name:str; lifecycle:str='DISCOVERED'; accuracy:float=0; speed:float=0; reliability:float=0; consistency:float=0; coverage:float=0; cost:float=0; risk:float=0

class SkillEvaluator:
    order=('DISCOVERED','LEARNING','PRACTICING','EVALUATING','COMPETENT','EXPERT','AUTONOMOUS')
    def promote(self, skill:Skill, evidence:Mapping[str,Any], approved:bool=False):
        if not approved or not evidence.get('sufficient',False): return skill
        i=self.order.index(skill.lifecycle); skill.lifecycle=self.order[min(i+1,len(self.order)-1)]; return skill

class CognitiveEngine:
    def learn(self, episodes:list[Episode]):
        successes=[e for e in episodes if e.outcome==Outcome.SUCCESS]; failures=[e for e in episodes if e.outcome==Outcome.FAILURE]
        return {'success_patterns':len(successes),'failure_patterns':len(failures),'observations':len(episodes),'requires_review':bool(failures)}
    def safety_check(self, candidate:LearningCandidate):
        return candidate.risk not in {'CRITICAL','SECURITY'} and candidate.approval_required
