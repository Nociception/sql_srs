-- themes: case_when count group_by
-- tables: season
-- subject: For each division (Div), count how many times Lille won (at home, or away). Read the notes_season.txt file.
-- TODO: Add a feature to display additionnal notes if necessary.

SELECT
    Div,
    COUNT (
        CASE 
            WHEN HomeTeam = 'Lille' AND FTHG > FTAG THEN 1 
        END
    ) AS lille_wins_home,
    COUNT (
        CASE 
            WHEN AwayTeam = 'Lille' AND FTHG < FTAG THEN 1 
        END
    ) AS lille_wins_away,
FROM season
GROUP BY Div
