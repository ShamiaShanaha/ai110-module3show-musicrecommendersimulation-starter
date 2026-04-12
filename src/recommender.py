from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a songs CSV and return a list of dicts with numeric fields cast to float/int."""
    import csv

    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id':           int(row['id']),
                'title':        row['title'],
                'artist':       row['artist'],
                'genre':        row['genre'],
                'mood':         row['mood'],
                'energy':       float(row['energy']),
                'tempo_bpm':    float(row['tempo_bpm']),
                'valence':      float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user profile (max 6.0 pts) and return (score, reasons)."""
  
    score = 0.0
    reasons = []

    # Tempo normalization constants derived from the dataset range (54 – 168 BPM)
    TEMPO_MIN = 54.0
    TEMPO_RANGE = 114.0  # 168 - 54

    # --- Step 1: Categorical scoring ---

    # Genre match: worth +1.0 pt — EXPERIMENT: halved from 2.0 to shift weight to energy
    if song['genre'] == user_prefs.get('favorite_genre'):
        score += 1.0                          # EXPERIMENT: was 2.0
        reasons.append('genre match (+1.0)')  # EXPERIMENT: was (+2.0)

    # Mood match: worth +1.0 pt — emotional intent
    if song['mood'] == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append('mood match (+1.0)')

    # --- Step 2: Numeric proximity scoring ---
    # Formula for each feature: pts = max_pts * (1 - |target - song_value|)
    # A song exactly at the target earns full points; further away earns fewer.

    # Energy: max 2.0 pts — EXPERIMENT: doubled from 1.0, now the strongest single signal
    energy_pts = 2.0 * (1.0 - abs(user_prefs.get('target_energy', 0.5) - song['energy']))  # EXPERIMENT: was 1.0
    score += energy_pts
    reasons.append(f'energy proximity (+{energy_pts:.2f})')

    # Acousticness: max 1.0 pt — wide dataset range (0.01–0.98), strong signal
    acousticness_pts = 1.0 * (1.0 - abs(user_prefs.get('target_acousticness', 0.5) - song['acousticness']))
    score += acousticness_pts
    reasons.append(f'acousticness proximity (+{acousticness_pts:.2f})')

    # Tempo: max 0.5 pt — normalized to [0, 1] before comparing
    user_tempo_norm = (user_prefs.get('target_tempo_bpm', 110) - TEMPO_MIN) / TEMPO_RANGE
    song_tempo_norm  = (song['tempo_bpm'] - TEMPO_MIN) / TEMPO_RANGE
    tempo_pts = 0.5 * (1.0 - abs(user_tempo_norm - song_tempo_norm))
    score += tempo_pts
    reasons.append(f'tempo proximity (+{tempo_pts:.2f})')

    # Valence: max 0.25 pt — narrowest range in dataset, used as tiebreaker
    valence_pts = 0.25 * (1.0 - abs(user_prefs.get('target_valence', 0.5) - song['valence']))
    score += valence_pts
    reasons.append(f'valence proximity (+{valence_pts:.2f})')

    # Danceability: max 0.25 pt — tiebreaker alongside valence
    dance_pts = 0.25 * (1.0 - abs(user_prefs.get('target_danceability', 0.5) - song['danceability']))
    score += dance_pts
    reasons.append(f'danceability proximity (+{dance_pts:.2f})')

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first, and return the top k as (song, score, explanation) tuples."""

    # Step 1 — Score every song using a list comprehension.
    # The nested `for score, reasons in [score_song(...)]` unpacks the
    # function's return tuple directly inside the comprehension.
    scored = [
        (song, score, ' | '.join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # Step 2 — Sort and slice in one chained expression.
    # sorted() returns a new list (no mutation). [:k] keeps only the top k.
    return sorted(scored, key=lambda entry: entry[1], reverse=True)[:k]
