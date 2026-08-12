"""Handoff and collaboration safety contracts."""
REQUIRED_HANDOFF_FIELDS=('objective','completed_work','remaining_work','evidence','assumptions','uncertainties','warnings','artifacts')

def validate_handoff(package:dict)->tuple[bool,list[str]]:
    missing=[k for k in REQUIRED_HANDOFF_FIELDS if k not in package]
    return not missing, missing

def authorized_delegation(*,scope:set[str],allowed:set[str],risk:str,approval:bool=False)->bool:
    if not scope.issubset(allowed): return False
    if risk in {'HIGH','CRITICAL'} and not approval: return False
    return True

def requires_independent_review(risk:str)->bool:
    return risk in {'HIGH','CRITICAL'}
