import copy
from typing import List

import boto3
import os

from src.story.domain.user import User
from src.story.domain.stage import Stage


class StoryClient:
    dyanmodb = boto3.resource('dynamodb')
    user_table = dyanmodb.Table(os.environ['USER_TABLE'])
    stage_table = dyanmodb.Table(os.environ['STAGE_TABLE'])

    def get_story(self, phone):
        result = self.user_table.get_item(Key={'phone': phone})
        print("Found story in dynamo: " + str(result))
        return result['Item']

    def get_stage(self, stage_id):
        result = self.stage_table.get_item(Key={'id': stage_id})
        print("Found stage in dynamo: " + str(result))
        return result['Item']

    def set_stage(self, user: User, stage_id):
        new_user = copy.deepcopy(user)
        new_user.user_state['current_stage'] = stage_id
        self.user_table.update_item(
            Key={
                'phone': new_user.phone
            },
            UpdateExpression='SET user_state = :new_state',
            ExpressionAttributeValues={
                ':new_state': new_user.user_state
            }
        )
        print("Updated user to " + str(new_user))
        return new_user

    def get_child_stages(self, children: List[str]) -> List[Stage]:
        return [Stage.from_dynamo(self.get_stage(stage)) for stage in children]
