# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
InTune

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

InTune suggests songs based on a user's preferred genre, mood, and audio features. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  
Every song in the catalog gets a score out of 6. The score is built from seven features. If the song's genre matches your favorte genre  it earns 1 point. If the mood matches it earns 1 more point. The remaining points come from how close the song audio values are. The songs are sorted from highest to lowest and thet top 5 are shown. 

Features:
1. Genre
2. Mood
3. Energy
4. Acousticness
5. Tempo
6. Valence
7. Danceability 

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  
There are 20 songs. The original file had 10, so I added 10 more songs. The dataset does not include non-Western genres.

Genre: 
- pop
- lofi 
- rock 
- ambient 
- jazz
- synthwave
- indie pop
- hip hop
- classical 
- r&b 
- electronic 
- folk 
- metal 
- reggae 
- soul 
- country 
- blues 

Moods: 
- happy 
- chill
- intense 
- relaxed 
- focused 
- moody 
- euphoric
- peaceful 
- romantic 
- melancholic 
- agry 
- nostalgic
- sad


Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

The system works best for lo-fi and pop users because those genres have more than one song. The scoring also does a reasonable job of cross-genre discovery. Every recommendation comes with a clear explanation of how the score was made, making the system easier to understand. 

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
The biggest weakness is that most genres only have one song. If you like metal, there is only one metal song that the system can recommend to you. After that, it only picks whatever sounds closest to your other preferences. This means a lot of metal fans and a lofi fan can end up with similar songs at the bottom of their list, even if their taste are different. There is also a gap when it comes to energy value between 0.62 and 0.74, with no songs in that range. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 
I tested on 6 user profiles. A high-energy pop lover got Sunrise City at the top, which makes sense since it is the only pop song that is also happy and energetic. A chill lo-fi listener got Midnight Coding first, which was expected. A rock listener got Storm Runner first since it is the only rock song. 

The last 3 were made to break the system. The first one had a sad mood, but wanted very high energy, which is a contradiction. No song could satisfy both at the same time, so every result had a weak score. The second one had a favorite genre that does not exist, so the system ignored the genre preference and recommended songs based on audio features without telling the user the genre was missing. The third one had every preference set to the middle value. Since everything was neutral, almost every song was scored the same, and the results felt random. 

I also tested what happened when I changed the scoring weight. I made energy worth double and genre worth half. For lofi and pop users, nothing changed at the top, but for rock users, high-energy songs from completely different genres started to appear in the top 5 just because their energy was close enough.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  
- The recommender system should be able to reject bad matches rather than always returning something, even if it doesn't match. 
- Genre matching should give partial points for similar genres instead of zero
- Adding more songs per genre would make the recommendation more useful 

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  
Writing the scoring code felt easy, but when testing it, I realized the system was giving bad recommendations to users who liked metal or blues because those genres had only one song in the catalog. The code was doing what it was supposed to do, but the results were still unfair. The output of my code looked very convincing, even though the system was simple. Before this project, I always wondered how apps like Spotify were recommending songs, and now I know they are just measuring distance. Every song gets compared to a target, and the closest one wins. There is no taste, no feeling, and no understanding of what makes a song good. It is just numbers being sorted. 

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
