from html import unescape

from alertserver.config import Trello as config_trello
import trolly

client = trolly.client.Client(config_trello.api_key, config_trello.token)
assert client is not None

member = client.get_member()
assert member is not None

print('Connected by Member: %s' % member.get_member_information()['email'])

board = client.get_board(id=config_trello.board_id)
assert board is not None

print('Board Name: %s' % board.get_board_information()['name'])


def post_activity(card_id: int, format_string: str, **kwargs):
    comment_body = format_string.format(**{
        **kwargs,
        'card_id': card_id
    }).replace('\\n', '\n').replace('\\t', '\t')
    card = board.get_card(str(card_id))
    assert card is not None
    card.add_comments(comment_body)


def post_branch_activity(card_id: int, branch_name: str, link: str):
    post_activity(card_id, config_trello.fms_branch, branch_name=branch_name, link=link)


def post_commit_activity(card_id: int, branch_name: str, commit_log: str, link: str):
    post_activity(card_id, config_trello.fms_commit, branch_name=branch_name, commit_log=commit_log, link=link)


def post_merge_activity(card_id: int, branch_name: str, link: str):
    post_activity(card_id, config_trello.fms_merge, branch_name=branch_name, link=link)

# post_branch_activity(255, 'develop', 'http://www.naver.com')
