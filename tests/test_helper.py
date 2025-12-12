import uuid

def get_unique_org_name():
    return f"TestOrg_{uuid.uuid4().hex[:8]}"

def get_unique_email():
    return f"admin_{uuid.uuid4().hex[:8]}@testorg.com"
