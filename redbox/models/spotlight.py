from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, computed_field, field_serializer

from redbox.models.file import File


class SpotlightTask(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    id: str
    title: str
    # langchain.prompts.PromptTemplate needs pydantic v1, breaks
    # https://python.langchain.com/docs/guides/pydantic_compatibility
    prompt_template: object

    created_datetime: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    def __hash__(self):
        return hash((type(self),) + (self.id, self.title))

    @computed_field
    def model_type(self) -> str:
        return self.__class__.__name__

    @field_serializer("prompt_template")
    def serialise_prompt(self, prompt_template: PromptTemplate, _info):
        if isinstance(prompt_template, PromptTemplate):
            return prompt_template.dict()
        else:
            return prompt_template


class SpotlightTaskComplete(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    id: str
    title: str
    # langchain.chains.base.Chain needs pydantic v1, breaks
    # https://python.langchain.com/docs/guides/pydantic_compatibility
    chain: object
    file_hash: str
    raw: str
    processed: Optional[str] = None
    created_datetime: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    creator_user_uuid: Optional[str]

    @computed_field
    def model_type(self) -> str:
        return self.__class__.__name__

    @field_serializer("chain")
    def serialise_chain(self, chain: Chain, _info):
        if isinstance(chain, Chain):
            return chain.dict()
        else:
            return chain


class Spotlight(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    files: List[File]
    file_hash: str
    created_datetime: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    tasks: List[SpotlightTask]

    @computed_field
    def model_type(self) -> str:
        return self.__class__.__name__

    def to_documents(self) -> List[str]:
        return [file.to_document() for file in self.files]


class SpotlightComplete(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    file_hash: str
    file_uuids: List[str]
    tasks: List[SpotlightTaskComplete]
    created_datetime: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    creator_user_uuid: Optional[str]

    @computed_field
    def model_type(self) -> str:
        return self.__class__.__name__
