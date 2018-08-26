from typing import Optional

from src.story.domain.user import User
from src.story.domain.stage import Stage
from src.story.db.story_client import StoryClient


class StoryService:
    client = StoryClient()

    def get_story(self, phone: str) -> User:
        return User.from_dynamo(self.client.get_story(phone))

    def get_stage(self, stage_id: str) -> Stage:
        return Stage.from_dynamo(self.client.get_stage(stage_id))

    def update_stage(self, user: User, stage: Stage):
        return self.client.set_stage(user, stage.id)

    def find_stage_by_phrase(self, stage: Stage, phrase: str) -> Optional[Stage]:
        children = self.client.get_child_stages(stage.children)
        print("Searching for Phrase: " + phrase.casefold() + " In children stages: " + str(children))
        for stage in children:
            if phrase.casefold() in stage.triggers.phrase:
                return stage
        return None
