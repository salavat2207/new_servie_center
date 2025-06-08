from fastapi import Depends, HTTPException, status
from app.auth import get_current_admin_user

def superadmin_required(current_user=Depends(get_current_admin_user)):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Только для суперадминов")
    return current_user