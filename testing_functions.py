def test_retrieve_player_stats_json():
    import json

    try:
        with open('player_stats.json', 'r') as json_file:
            p_stats = json.load(json_file)

            print(tuple(p_stats['coords'].values()))

    except Exception as e:
        print('Error parsing player stats: ', e)


if __name__ == '__main__':
    test_retrieve_player_stats_json()