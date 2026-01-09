from pydantic import BaseModel, Field
from typing import List, Optional

class ProfiloUtente(BaseModel):
    generi: List[str] = Field(default_factory=list, description="Generi musicali preferiti")
    artisti: List[str] = Field(default_factory=list, description="Artisti citati o preferiti")
    budget_max: Optional[float] = Field(None, description="Budget massimo per i concerti")
    localita: Optional[str] = Field(None, description="Città o area geografica dell'utente")
    note: Optional[str] = Field(None, description="Altre preferenze (es. strumenti, atmosfere)")
