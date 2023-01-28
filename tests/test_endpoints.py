from datetime import datetime
from unittest import TestCase

from ossapi import (RankingType, BeatmapsetEventType, AccessDeniedError,
    InsufficientScopeError, Mod, GameMode)

from tests import (
    TestCaseAuthorizationCode, TestCaseDevServer, UNIT_TEST_MESSAGE,
    api_v2 as api,
    api_v2_full as api_full,
    api_v2_dev as api_dev
)


class TestBeatmapsetDiscussionPosts(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussion_posts()

class TestUserRecentActivity(TestCase):
    def test_deserialize(self):
        api.user_recent_activity(12092800)

class TestSpotlights(TestCase):
    def test_deserialize(self):
        api.spotlights()

class TestUserBeatmaps(TestCase):
    def test_deserialize(self):
        api.user_beatmaps(user_id=12092800, type_="most_played")

class TestUserKudosu(TestCase):
    def test_deserialize(self):
        api.user_kudosu(user_id=3178418)

class TestBeatmapScores(TestCase):
    def test_deserialize(self):
        api.beatmap_scores(beatmap_id=1981090)

class TestBeatmap(TestCase):
    def test_deserialize(self):
        api.beatmap(beatmap_id=221777)

        # beatmap with a diff owner
        bm = api.beatmap(beatmap_id=1604098)
        # might need to be updated when
        # https://github.com/ppy/osu-web/issues/9784 is addressed.
        self.assertIsNone(bm.owner)

class TestBeatmapset(TestCase):
    def test_deserialize(self):
        api.beatmapset(beatmap_id=3207950)

class TestBeatmapsetEvents(TestCase):
    def test_deserialize(self):
        api.beatmapset_events()

    def test_all_types(self):
        # beatmapset_events is a really complicated endpoint in terms of return
        # types. We want to make sure both that we're not doing anything wrong,
        # and the osu! api isn't doing anything wrong by returning something
        # that doesn't match their documentation.
        for event_type in BeatmapsetEventType:
            api.beatmapset_events(types=[event_type])

class TestRanking(TestCase):
    def test_deserialize(self):
        api.ranking("osu", RankingType.PERFORMANCE, country="US")

class TestUserScores(TestCase):
    def test_deserialize(self):
        api.user_scores(12092800, "best")

class TestBeatmapUserScore(TestCase):
    def test_deserialize(self):
        api.beatmap_user_score(beatmap_id=221777, user_id=2757689, mode="osu")

class TestBeatmapUserScores(TestCase):
    def test_deserialize(self):
        api.beatmap_user_scores(beatmap_id=221777, user_id=2757689, mode="osu")

class TestSearch(TestCase):
    def test_deserialize(self):
        api.search(query="peppy")

class TestComment(TestCase):
    def test_deserialize(self):
        api.comment(comment_id=1)

class TestDownloadScore(TestCase):
    def test_deserialize(self):
        # api instance is using client credentials which doesn't have access to
        # downloading replays
        self.assertRaises(AccessDeniedError,
            lambda: api.download_score(mode="osu", score_id=2797309065))

class TestSearchBeatmaps(TestCase):
    def test_deserialize(self):
        api.search_beatmapsets(query="the big black")

class TestUser(TestCase):
    def test_deserialize(self):
        api.user(12092800)

    def test_key(self):
        # make sure it automatically falls back to username if not specified
        api.user("tybug2")
        api.user("tybug2", key="username")

        self.assertRaises(Exception, lambda: api.user("tybug2", key="id"))

class TestMe(TestCase):
    def test_insufficient_scope(self):
        # client credentials api can't request `Scope.IDENTIFY` and so can't
        # access /me
        self.assertRaises(InsufficientScopeError, api.get_me)

class TestWikiPage(TestCase):
    def test_deserialize(self):
        api.wiki_page("en", "Welcome")

class TestChangelogBuild(TestCase):
    def test_deserialize(self):
        api.changelog_build("stable40", "20210520.2")

class TestChangelogListing(TestCase):
    def test_deserialize(self):
        api.changelog_listing()

class TestChangelogLookup(TestCase):
    def test_deserialize(self):
        api.changelog_lookup("lazer")

class TestForumTopic(TestCase):
    def test_deserialize(self):
        api.forum_topic(141240)

class TestBeatmapsetDiscussionVotes(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussion_votes().votes[0].score

class TestBeatmapsetDiscussions(TestCase):
    def test_deserialize(self):
        api.beatmapset_discussions()

class TestNewsListing(TestCase):
    def test_deserialize(self):
        api.news_listing(year=2021)

class TestNewsPost(TestCase):
    def test_deserialize(self):
        # querying the same post by id or slug should give the same result.
        post1 = api.news_post(1025, key="id")
        post2 = api.news_post("2021-10-04-halloween-fanart-contest", key="slug")

        self.assertEqual(post1.id, post2.id)
        self.assertEqual(post1, post2)

class TestSeasonalBackgrounds(TestCase):
    def test_deserialize(self):
        api.seasonal_backgrounds()

class TestBeatmapAttributes(TestCase):
    def test_deserialize(self):
        api.beatmap_attributes(221777, ruleset="osu")
        api.beatmap_attributes(221777, mods=Mod.HDDT)
        api.beatmap_attributes(221777, mods="HR")
        api.beatmap_attributes(221777, ruleset_id=0)

class TestUsers(TestCase):
    def test_deserialize(self):
        api.users([12092800])

class TestBeatmaps(TestCase):
    def test_deserialize(self):
        api.beatmaps([221777])

class TestScore(TestCase):
    def test_deserialize(self):
        # downloadable
        api.score(GameMode.OSU, 2243145877)
        # downloadable, my score
        api.score(GameMode.OSU, 3685255338)
        # not downloadable, my score
        api.score(GameMode.OSU, 3772000814)

        # other gamemodes
        api.score(GameMode.TAIKO, 176904666)
        api.score(GameMode.MANIA, 524674141)
        api.score(GameMode.CATCH, 211167989)

class TestFriends(TestCase):
    def test_access_denied(self):
        self.assertRaises(InsufficientScopeError, api.friends)


# ======================
# api_full test cases
# ======================

class TestCreateNewPM(TestCaseAuthorizationCode):
    def test_deserialize(self):
        # test_account https://osu.ppy.sh/users/14212521
        api_full.send_pm(14212521, UNIT_TEST_MESSAGE)

class TestMeAuth(TestCaseAuthorizationCode):
    def test_deserialize(self):
        api_full.get_me()

class TestFriendsAuth(TestCaseAuthorizationCode):
    def test_deserialize(self):
        api_full.friends()



# =====================
# api_dev test cases
# =====================

class TestForumCreate(TestCaseDevServer):
    def test_create(self):
        # test creating both a topic and posting a reply in that topic.
        # be careful to post to one of the forums in
        # `double_post_allowed_forum_ids`, or else we'll be rejected for double
        # posting.
        # https://github.com/ppy/osu-web/blob/3d1586392102b05f2a3b264905c4dbb7b
        # 2d430a2/config/osu.php#L107.
        response = api_dev.forum_create_topic(UNIT_TEST_MESSAGE, 52,
            UNIT_TEST_MESSAGE)
        topic_id = response.topic.id
        api_dev.forum_reply(topic_id, UNIT_TEST_MESSAGE)

    def test_create_with_poll(self):
        poll = {
            "options": ["Option 1", "Option 2"],
            "title": "Test Poll",
            "length_days": 0,
            "vote_change": True,
            "max_options": 1,
        }
        api_dev.forum_create_topic(
            title=f"{UNIT_TEST_MESSAGE}",
            body=f"{UNIT_TEST_MESSAGE} ({datetime.now()})",
            forum_id=78,
            with_poll=True, poll=poll
        )

class TestForumEdit(TestCaseDevServer):
    def test_edit(self):
        # create a new topic and post
        response = api_dev.forum_create_topic(UNIT_TEST_MESSAGE, 52,
            UNIT_TEST_MESSAGE)
        topic_id = response.topic.id
        response = api_dev.forum_reply(topic_id, UNIT_TEST_MESSAGE)
        post_id = response.id

        # edit both the topic and post
        api_dev.forum_edit_topic(topic_id,
            f"This title was last updated at {datetime.now()}")
        api_dev.forum_edit_post(post_id,
            f"This comment was last edited at {datetime.now()}")
