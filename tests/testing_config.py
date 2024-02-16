

from dotenv import dotenv_values



_test_env_path = 'tests/testing.env'
testing_config = dotenv_values(_test_env_path)

print(testing_config['TEST_DB_URL'])
# Тестовые Tables отличаются ограничениями на дефолтные
# значения, так как в рабочих Tables они не назначены
# ввиду конфликтов этих значений с уже существующими
# отдампленными таблицами



# @dataclass
# class TestConfig:
#     test_db_url: str
#
#
# def load_config(path: Optional[str] = None) -> TestConfig:
#     env = Env()
#     env.read_env(path)
#     return TestConfig(
#         test_db_url=env("TEST_DB_URL"),
#
#     )
