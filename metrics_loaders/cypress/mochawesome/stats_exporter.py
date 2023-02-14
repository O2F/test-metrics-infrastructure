import stats_handler.stats_extractor as se
import stats_handler.stats_db_writer as sw


def main():
    stats_extractor = se.StatsExtractor()
    stats_extractor.extract_stats_from_results_to_file()

    stats = stats_extractor.extract_stats_from_results()

    stats_to_db = sw.StatsIngestion()
    stats_to_db.insert_stats_from_dict(stats)


if __name__ == "__main__":
    main()
