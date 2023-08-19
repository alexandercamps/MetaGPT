#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 22:12
@Author  : alexanderwu
@File    : environment.py
"""
import asyncio
from typing import Iterable

from pydantic import BaseModel, Field

from metagpt.memory import Memory
from metagpt.roles import Role
from metagpt.schema import Message


class Environment(BaseModel):
    """Environment, bearing a batch of roles, roles can publish messages to the environment, and can be observed by other roles
       Environment, hosting a batch of roles, roles can publish messages to the environment, and can be observed by other roles
    
    """

    roles: dict[str, Role] = Field(default_factory=dict)
    memory: Memory = Field(default_factory=Memory)
    history: str = Field(default='')

    class Config:
        arbitrary_types_allowed = True

    def add_role(self, role: Role):
        """Add a role in the current environment
           Add a role in the current environment
        """
        role.set_env(self)
        self.roles[role.profile] = role

    def add_roles(self, roles: Iterable[Role]):
        """Add a batch of characters in the current environment
            Add a batch of characters in the current environment
        """
        for role in roles:
            self.add_role(role)

    def publish_message(self, message: Message):
        """Post information to the current environment
          Post information to the current environment
        """
        # self.message_queue.put(message)
        self.memory.add(message)
        self.history += f"\n{message}"

    async def run(self, k=1):
        """Process all Role runs at once
        Process all Role runs at once
        """
        # while not self.message_queue.empty():
        # message = self.message_queue.get()
        # rsp = await self.manager.handle(message, self)
        # self.message_queue.put(rsp)
        for _ in range(k):
            futures = []
            for role in self.roles.values():
                future = role.run()
                futures.append(future)

            await asyncio.gather(*futures)

    def get_roles(self) -> dict[str, Role]:
        """Get all the roles in the environment
           Process all Role runs at once
        """
        return self.roles

    def get_role(self, name: str) -> Role:
        """Get a specified role within the environment
           Get all the environment roles
        """
        return self.roles.get(name, None)
