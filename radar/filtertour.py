filterteam = {'Berlin International': 'Big', 'Elevate^': 'Elevate', 'Barça': 'Barca', 'Five Media': 'Five Media Clan', 'Grp': 'Grypciocraft',
               'Hle Challengers': 'Hanwha Life Challengers', 'Kt Rolster': 'Kt Rolster Challengers', 'Drx': 'Drx Challengers', 'Vitality Bee': 'Vitality.Bee'}


"""
UPDATE datakofs
SET tour_name = (
    SELECT COALESCE(
        (
            SELECT tour_name
            FROM datakofs AS t2
            WHERE t2.bk_name = 'Fonbet'
                AND t2.team1 = datakofs.team1
                AND t2.team2 = datakofs.team2
                AND t2.date_match BETWEEN (datakofs.date_match - INTERVAL '1 hour') AND (datakofs.date_match + INTERVAL '1 hour')
            LIMIT 1
        ),
        tour_name
    )
)
WHERE bk_name = 'Cloudbet';
"""