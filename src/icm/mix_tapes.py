from icm.spotify import spotify_auth

from logging import getLogger

LOG = getLogger(__name__)

class MixTapeBuilder:

    def __init__(self, username):
        self.username = username
        self.sp = spotify_auth()

    def _find_spotify_track(self, track, artist):
        query = f"track:{track} artist:{artist}"
        LOG.info(f"Searching for {track} {artist}")
        results = self.sp.search(query, type="track", market="US")
        if results['tracks']['items']:
            # print(json.dumps(results['tracks']['items'][0], indent=2))
            result = results['tracks']['items'][0]
            artists_str = ", ".join([artist["name"] for artist in result["artists"]])
            LOG.info("Found track: {name} -- {artists_str} <id:{id}>".format(artists_str=artists_str, **result))
            return results['tracks']['items'][0]["id"]
        else:
            LOG.warning("No search results!")

    def _process_track(self, track, tape: dict):
        track_tuple = track.split('--')
        title = track_tuple[0].strip()
        artist = tape.get('artist') or track_tuple[1].strip()
        return self._find_spotify_track(title, artist)

    def _process_mix_tape(self, tape, min_hit_rate, dryrun):
        LOG.info("Processing mix tape {id}: {title}".format(**tape))
        tracks = tape["side_a"] + tape["side_b"]
        spotify_tracks = [self._process_track(track, tape) for track in tracks]
        spotify_tracks = list(filter(None, spotify_tracks))

        if len(spotify_tracks) < len(tracks) * min_hit_rate:
            LOG.warning(f"Aborting playlist creation because only {len(spotify_tracks)} of {len(tracks)} tracks found")

        new_playlist_name = "{title} - ICM-{id}".format(**tape)

        if dryrun:
            LOG.info(f"Would create playlist '{new_playlist_name}' with {len(spotify_tracks)} tracks")
        else:
            playlist = self.sp.user_playlist_create(self.username, name=new_playlist_name)
            self.sp.user_playlist_add_tracks(self.username, playlist["id"], tracks=spotify_tracks)
            tape["spotify_playlist"] = playlist["id"]
            LOG.info(f"Created playlist '{new_playlist_name}' with {len(spotify_tracks)} tracks")

    def process_tape_list(self, tape_list, min_hit_rate, dryrun):
        for tape in tape_list:
            if "spotify_playlist" in tape:
                LOG.info("Skipping mix tape {id}: {title} (already has playlist {spotify_playlist}".format(**tape))
                continue
            self._process_mix_tape(tape, min_hit_rate, dryrun)
