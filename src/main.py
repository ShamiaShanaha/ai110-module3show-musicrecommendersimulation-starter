"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_results(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a formatted results block for one user profile."""
    print("\n" + "=" * 55)
    print(f"  {profile_name}")
    print(f"  Genre: {user_prefs['favorite_genre'].upper()}  |  Mood: {user_prefs['favorite_mood'].upper()}")
    print("=" * 55)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = int((score / 6.0) * 20)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Score: {score:.2f} / 6.00  [{bar}]")
        print("       Why:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        # ----------------------------------------------------------------
        # Standard profiles
        # ----------------------------------------------------------------
        (
            "PROFILE 1 — HIGH-ENERGY POP",
            {
                "favorite_genre":     "pop",
                "favorite_mood":      "happy",
                "target_energy":      0.85,
                "target_acousticness":0.10,
                "target_tempo_bpm":   125,
                "target_valence":     0.82,
                "target_danceability":0.85,
            },
        ),
        (
            "PROFILE 2 — CHILL LOFI",
            {
                "favorite_genre":     "lofi",
                "favorite_mood":      "chill",
                "target_energy":      0.40,
                "target_acousticness":0.75,
                "target_tempo_bpm":   78,
                "target_valence":     0.58,
                "target_danceability":0.60,
            },
        ),
        (
            "PROFILE 3 — DEEP INTENSE ROCK",
            {
                "favorite_genre":     "rock",
                "favorite_mood":      "intense",
                "target_energy":      0.91,
                "target_acousticness":0.10,
                "target_tempo_bpm":   152,
                "target_valence":     0.48,
                "target_danceability":0.66,
            },
        ),
        # ----------------------------------------------------------------
        # Adversarial / edge case profiles
        # ----------------------------------------------------------------
        (
            "EDGE CASE 1 — CONFLICTING: SAD MOOD + HIGH ENERGY",
            {
                # Blues/sad is the category preference, but all numeric targets
                # point at high-intensity electronic music. No single song can
                # satisfy both halves — the scorer gets pulled in two directions.
                "favorite_genre":     "blues",
                "favorite_mood":      "sad",
                "target_energy":      0.92,   # blues songs are low energy which is a  direct conflict
                "target_acousticness":0.05,   # blues is acoustic which is a direct conflict
                "target_tempo_bpm":   160,    # sad songs are slow which is a direct conflict
                "target_valence":     0.20,   # consistent with sad
                "target_danceability":0.90,   # sad songs rarely danceable which is a conflict
            },
        ),
        (
            "EDGE CASE 2 — GHOST GENRE: FAVORITE NOT IN CATALOG",
            {
                # 'k-pop' does not exist in songs.csv, so genre_score is always
                # 0.0 for every song. The entire ranking falls back to numeric
                # proximity alone — genre weight is completely wasted.
                "favorite_genre":     "k-pop",
                "favorite_mood":      "euphoric",
                "target_energy":      0.88,
                "target_acousticness":0.05,
                "target_tempo_bpm":   130,
                "target_valence":     0.85,
                "target_danceability":0.92,
            },
        ),
        (
            "EDGE CASE 3 — PERFECTLY NEUTRAL: ALL MIDPOINTS",
            {
                # Every numeric target sits at the midpoint of its range.
                # All songs receive nearly identical numeric scores, so the
                # categorical match (genre/mood) becomes the only differentiator.
                "favorite_genre":     "ambient",
                "favorite_mood":      "peaceful",
                "target_energy":      0.50,
                "target_acousticness":0.50,
                "target_tempo_bpm":   111,    # midpoint of dataset range (54–168)
                "target_valence":     0.50,
                "target_danceability":0.50,
            },
        ),
    ]

    print("\n" + "=" * 55)
    print("  MUSIC RECOMMENDER SIMULATION")
    print(f"  Catalog: {len(songs)} songs  |  Top 5 per profile  |  Max score: 6.0")
    print("=" * 55)

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_results(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
