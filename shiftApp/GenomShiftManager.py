import random
import time
from typing import List, Dict, Any, Set


class GenomShiftConst:
    REST_TYPE: int = -1


class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


class GenomShift:
    # user0 user1
    # [0, 1] Day
    # [0, 1]
    # [0, 1]
    # [0, 1]
    v_shift: List[List[int]]
    #         Day
    # user0: [0,0,0,0,0,0,0,0,0,0,0],
    # user1: [1,1,1,1,1,1,1,1,1,1,1],
    h_shift: List[List[int]]

    # 数値が高い方が悪い
    loss: float = 0.0
    # list [{int,int}, {int,int}]
    error_line: List[set]

    total_work_time_list: List[float]
    total_work_time_avg: float

    def __init__(self, v_shift: List[List[int]]):
        self.v_shift = v_shift
        self.h_shift = self.shift_transform(v_shift)
        self.error_line = [set() for _ in range(len(self.h_shift))]

    def get_v_shift(self) -> List[List[int]]:
        return self.v_shift

    def get_h_shift(self) -> List[List[int]]:
        return self.h_shift

    def get_loss(self) -> float:
        return self.loss

    def get_error_line(self) -> List[set]:
        return self.error_line

    def get_total_work_time_list(self) -> List[float]:
        return self.total_work_time_list

    def get_total_work_time_avg(self) -> float:
        return self.total_work_time_avg

    def set_v_shift(self, v_shift: List[List[int]]):
        self.v_shift = v_shift
        self.h_shift = self.shift_transform(v_shift)

    def set_h_shift(self, h_shift: List[List[int]]):
        self.h_shift = h_shift
        self.v_shift = self.shift_transform(h_shift)

    def set_loss(self, loss: float):
        self.loss = loss

    def set_error_line(self, error_line: List[Set[int]]):
        self.error_line = error_line

    def set_total_work_time_list(self, total_work_time_list: List[float]):
        self.total_work_time_list = total_work_time_list

    def set_total_work_time_avg(self, total_work_time_avg: float):
        self.total_work_time_avg = total_work_time_avg

    def add_loss(self, loss: float):
        self.loss += loss

    def shift_transform(self, shift: List[List[int]]):
        return [[l[i] for l in shift] for i in range(len(shift[0]))]


class ShiftConfig:
    # int 1 < x
    day_length: int
    # int 1 < x
    max_work_day: int
    # int
    rest_type: List[int]
    # int
    night_type: List[int]
    # dict {str: int}
    work_type_time: Dict[int, float]
    # dict {int: [str, str], int: [str, str]}
    shift_pattern_dict: Dict[int, List[int]]
    # list [[int, int], [int, int]]
    rest_requests: List[List[int]]
    # list [int, int]
    shift_pattern: List[int]
    # boolean
    debug: bool

    def __init__(
            self, day_length: int, max_work_day: int,
            rest_type: List[int], night_type: List[int], work_type_time: Dict[int, float],
            shift_pattern_dict: Dict[int, List[int]], rest_requests: List[List[int]], shift_pattern: List[int], debug: bool = False):

        self.day_length = day_length if day_length > 1 else 7
        self.max_work_day = max_work_day if max_work_day > 1 else 6
        self.rest_type = rest_type if rest_type else [-1]
        self.night_type = night_type
        work_type_time.update({-1: 0.0})
        self.work_type_time = work_type_time
        shift_pattern_dict.update({-1: [-1]})
        for key in shift_pattern_dict:
            shift_pattern_dict[key] = shift_pattern_dict[key] if shift_pattern_dict[key] else [-1]
        self.shift_pattern_dict = shift_pattern_dict
        self.rest_requests = rest_requests if rest_requests else []
        self.shift_pattern = shift_pattern if shift_pattern else [0 for _ in range(day_length)]
        self.debug = debug

    def get_day_length(self) -> int:
        return self.day_length

    def get_max_work_day(self) -> int:
        return self.max_work_day

    def get_rest_type(self) -> List[int]:
        return self.rest_type

    def get_night_type(self) -> List[int]:
        return self.night_type

    def get_tork_type_time(self) -> Dict[int, float]:
        return self.work_type_time

    def get_shift_pattern_dict(self) -> Dict[int, List[int]]:
        return self.shift_pattern_dict

    def get_rest_requests(self) -> List[List[int]]:
        return self.rest_requests

    def get_shift_pattern(self) -> List[int]:
        return self.shift_pattern

    def get_shift_pattern_by_day(self, day: int) -> List[int]:
        return self.shift_pattern_dict[self.shift_pattern[day]]


class GenomShiftManager:

    ELITE_LENGTH: int = 20
    SHIFT_LENGTH: int = 100
    INDIVIDUAL_MUTATION: float = 0.50
    DAY_MUTATION: float = 0.08
    MAX_COUNT: int = 512
    # MAX_COUNT: int = 10
    MAX_GENERATION: int = 100000

    # class ShiftConfig
    shift_config: ShiftConfig
    # list [GenomShift]
    genom_shift_list: List[GenomShift] = []
    # list [GenomShift]
    elite_shift: List[GenomShift] = []
    # list [GenomShift]
    children_shift: List[GenomShift] = []

    def __init__(self, shift_config):
        self.shift_config = shift_config
        self.genom_shift_list = self.create_genom_shift_list(self.SHIFT_LENGTH)

    def get_shift_config(self) -> ShiftConfig:
        return self.shift_config

    def get_genom_shift_list(self) -> List[GenomShift]:
        return self.genom_shift_list

    def get_elite_shift(self) -> List[GenomShift]:
        return self.elite_shift

    def get_children_shift(self) -> List[GenomShift]:
        return self.children_shift

    def set_shift_config(self, shift_config: ShiftConfig):
        self.shift_config = shift_config

    def set_genom_shift_list(self, genom_shift_list: List[GenomShift]):
        self.genom_shift_list = genom_shift_list

    def set_elite_shift(self, elite_shift: List[GenomShift]):
        self.elite_shift = elite_shift

    def set_children_shift(self, children_shift: List[GenomShift]):
        self.children_shift = children_shift

    # 新規生成
    def create_genom_shift_list(self, shift_length: int) -> List[GenomShift]:
        return [self.create_genom_shift() for _ in range(shift_length)]

    def create_genom_shift(self) -> GenomShift:
        day_length: int = self.get_shift_config().get_day_length()
        v_shift: List[List[int]] = [self.create_random_v_shift_by_work_pattern(day) for day in range(day_length)]
        return GenomShift(v_shift)

    def create_random_v_shift_by_work_pattern(self, day: int) -> List[int]:
        pattern: List[int] = self.get_shift_config().get_shift_pattern_by_day(day)
        return random.sample(pattern, len(pattern))

    # 選別
    def select(self):
        # トーナメント式
        # ランダムに選手を選択し、ソートする
        selected_shift: List[GenomShift] = random.sample(self.get_genom_shift_list(), self.ELITE_LENGTH * 3)
        sorted_shift: List[GenomShift] = sorted(selected_shift, reverse=False, key=lambda u: u.get_loss())
        self.elite_shift = sorted_shift[:self.ELITE_LENGTH]

    # 交叉
    def crossover(self):
        children_shift: List[GenomShift] = []
        elite_shift: List[GenomShift] = self.elite_shift
        for i in range(self.ELITE_LENGTH):
            children_shift.extend(self._crossover(elite_shift[i - 1], elite_shift[i]))
        self.children_shift = children_shift

    def _crossover(self, blue: GenomShift, red: GenomShift) -> List[GenomShift]:
        # 一点交叉式
        crosspoint: int = random.randint(0, self.shift_config.get_day_length())
        blue_shift: List[List[int]] = blue.get_v_shift()
        red_shift: List[List[int]] = red.get_v_shift()
        first_child: List[List[int]] = blue_shift[:crosspoint] + red_shift[crosspoint:]
        second_child: List[List[int]] = red_shift[:crosspoint] + blue_shift[crosspoint:]
        return [GenomShift(first_child), GenomShift(second_child)]

    # 変異
    def mutation(self):
        for genom_shift in self.get_genom_shift_list():
            # INDIVIDUAL_MUTATIONの確率で変異対象となる
            if self.INDIVIDUAL_MUTATION > (random.randint(0, 100) / 100):
                self._day_mutation(genom_shift)

    def _day_mutation(self, genom_shift: GenomShift):
        mutation_shift: List[List[int]] = []
        v_shift = genom_shift.get_v_shift()
        for day, shift in enumerate(v_shift):
            # DAY_MUTATIONの確率で変異する
            if self.DAY_MUTATION > (random.randint(0, 100) / 100):
                mutation_shift.append(self.create_random_v_shift_by_work_pattern(day))
            else:
                mutation_shift.append(shift)
        genom_shift.set_v_shift(mutation_shift)

    # 評価
    def evaluation(self):
        for genom_shift in self.get_genom_shift_list():
            self.check_rest_requests(genom_shift)
            self.check_work_time(genom_shift)
            self.check_max_work_day(genom_shift)
            self.check_night_shfit(genom_shift)

    # 希望休は取れているか
    def check_rest_requests(self, genom_shift: GenomShift):
        point: float = 0.5
        h_shift: List[List[int]] = genom_shift.get_h_shift()
        loss: float = genom_shift.get_loss()
        rest_requests: List[List[int]] = self.shift_config.get_rest_requests()
        rest_type: List[int] = self.shift_config.get_rest_type()

        def _check_rest_requests(index: int, day: int):
            error_line: List[set] = genom_shift.get_error_line()
            error_line[index].add(day)
            genom_shift.set_error_line(error_line)
            return point

        for i, days in enumerate(rest_requests):
            loss += sum([_check_rest_requests(i, day) for day in days if h_shift[i][day] not in rest_type])
        genom_shift.set_loss(loss)

    # 平均的な勤務時間かどうか
    def check_work_time(self, genom_shift: GenomShift):
        loss: float = genom_shift.get_loss()
        total_work_time_list: List[float] = [self._count_work_time(shift) for shift in genom_shift.get_h_shift()]
        work_time_avg: float = sum(total_work_time_list) / len(total_work_time_list)
        loss += sum([abs(work_time_avg - time) / 100 for time in total_work_time_list])
        genom_shift.set_loss(loss)
        genom_shift.set_total_work_time_list(total_work_time_list)
        genom_shift.set_total_work_time_avg(work_time_avg)

    def _count_work_time(self, shift: List[int]) -> float:
        work_type_time = self.shift_config.get_tork_type_time()
        work_time = [work_type_time[v] for v in shift]
        return sum(work_time)

    # n連続勤務後に休みは取れているかどうか
    def check_max_work_day(self, genom_shift: GenomShift):
        point = 1
        # loss = genom_shift.get_loss()
        h_shift = genom_shift.get_h_shift()
        max_work_day = self.get_shift_config().get_max_work_day() + 1
        rest_type = self.get_shift_config().get_rest_type()
        rest_type_set = set(rest_type)
        step_range = range(max_work_day, len(h_shift[0]))

        def _check_max_work_day(i, index):
            error_line = genom_shift.get_error_line()
            _ = [error_line[index].add(error) for error in range(i - max_work_day, i)]
            genom_shift.set_error_line(error_line)
            return point
        loss: float = sum([sum([_check_max_work_day(i, index) for i in step_range if not bool(
            rest_type_set & set(shift[i - max_work_day:i]))]) for index, shift in enumerate(h_shift)])
        # print(step_range)
        genom_shift.add_loss(loss)

    # 夜勤後に休みはあるか
    def check_night_shfit(self, genom_shift: GenomShift):
        point: float = 1.0
        loss: float = genom_shift.get_loss()
        h_shift: List[List[int]] = genom_shift.get_h_shift()
        night_type: List[int] = self.get_shift_config().get_night_type()
        rest_type: List[int] = self.get_shift_config().get_rest_type()

        def _check_night_shfit(i: int, index: int) -> float:
            error_line = genom_shift.get_error_line()
            error_line[index].add(i)
            genom_shift.set_error_line(error_line)
            return point

        def _rest_check(i: int, shift: List[int]) -> bool:
            return shift[i - 1] in night_type and shift[i] not in rest_type

        loss += sum([sum([_check_night_shfit(i, index) for i in range(1, len(shift)) if _rest_check(i, shift)])
                     for index, shift in enumerate(h_shift)])
        genom_shift.set_loss(loss)

    # 世代交代
    def generation_change(self):
        sorted_shift = sorted(self.get_genom_shift_list(), reverse=False, key=lambda u: u.get_loss())
        new_shift_int = len(self.elite_shift) + len(self.children_shift)
        new_shift_list = sorted_shift[:new_shift_int] + self.elite_shift + self.children_shift
        self.set_genom_shift_list(new_shift_list)

    def execute(self):
        last_min = None
        count = 0
        for i in range(self.MAX_GENERATION):
            self.mutation()
            self.evaluation()

            fits = [i.get_loss() for i in self.get_genom_shift_list()]
            min_ = min(fits)
            max_ = max(fits)
            avg_ = sum(fits) / len(fits)
            if last_min is None or last_min > min_:
                last_min = min_
                count = 0
            if last_min <= 0:
                break
            count += 1
            if count >= self.MAX_COUNT:
                break
            if i % 100 == 0:
                self.evaluation()
                print("-----第{}世代の結果-----".format(i))
                print("  Min:{}".format(min_))
                print("  Max:{}".format(max_))
                print("  Avg:{}".format(avg_))
                print('  Cnt:{}'.format(count))
            self.select()
            self.crossover()
            self.generation_change()

        if self.get_shift_config().debug:
            self.debug_print()

        return self.get_best_shift()

    def get_best_shift(self) -> GenomShift:
        self.evaluation()
        return sorted(self.get_genom_shift_list(), reverse=False, key=lambda u: u.get_loss())[0]

    def debug_print(self):
        best = self.get_best_shift()
        h_shift = best.get_h_shift()
        loss = best.get_loss()
        error_line = best.get_error_line()
        total_work_time_avg = best.get_total_work_time_avg()
        total_work_time_list = best.get_total_work_time_list()
        rest_type = self.get_shift_config().get_rest_type()
        night_type = self.get_shift_config().get_night_type()
        max_work_day = self.get_shift_config().get_max_work_day()
        rest_requests = self.get_shift_config().get_rest_requests()
        shift_pattern = self.get_shift_config().get_shift_pattern()
        shift_pattern_dict = self.get_shift_config().get_shift_pattern_dict()
        print(f'--------------------------------------')

        # 総合評価
        print(f'Loss: {loss}')

        # 平均勤務時間
        print(f'Work Time Avg: {total_work_time_avg}')

        # 休み型
        print(f'Rest Type: {rest_type}')

        # 夜勤型
        print(f'Night Type: {night_type}')

        # 最高勤務
        print(f'Max Work Day: {max_work_day}')

        # シフトパターン内容
        print(f'Sfhit Pattern:')
        for key, val in shift_pattern_dict.items():
            print(f'{key}: {val}')

        # 希望休
        print(f'Rest Requests:')
        for i, rest in enumerate(rest_requests):
            print(f'{i}: {rest}')

        # 欠陥箇所
        print(f'Errors:')
        for i, error in enumerate(error_line):
            print(f'{i}: {sorted(error) if len(error) > 0 else "OK"}')

        # 完成シフトをコンソールに表示
        print(' - ' + ' '.join([str(i).rjust(2) for i in range(self.get_shift_config().day_length)]))
        for i, shift in enumerate(h_shift):
            line = f'{str(i).rjust(2)} '
            for j, s in enumerate(shift):
                if j in error_line[i]:
                    line += str(Color.RED + str(s).rjust(2) + Color.END + ' ')
                elif j in rest_requests[i]:
                    line += str(Color.GREEN + str(s).rjust(2) + Color.END + ' ')
                else:
                    line += str(str(s).rjust(2) + ' ')
            print(f'{line} {total_work_time_list[i]}')

        # シフトパターン
        print('   ' + ' '.join([str(i).rjust(2) for i in shift_pattern]))


if __name__ == '__main__':
    start_time: float = time.time()
    day_length: int = 28
    max_work_day: int = 6
    A: int = 1
    B: int = 2
    C: int = 3
    X: int = 4
    rest_type = [X]
    night_type = [B]
    shift_pattern_0 = [A, A, B, X, X]
    shift_pattern_1 = [A, B, X, X, X]
    shift_pattern_2 = [A, X, X, X, X]
    shift_pattern_dict: Dict[int, List[int]] = {
        0: shift_pattern_0,
        1: shift_pattern_1,
        2: shift_pattern_2,
    }

    shift_pattern: List[int] = random.choices(list(shift_pattern_dict.keys()), k=day_length)
    work_type_time: Dict[int, float] = {
        A: 8.0,
        B: 12.0,
        X: 0.0,
    }
    rest_requests = [sorted(random.sample(range(day_length), 5)) for _ in range(len(shift_pattern_0))]

    params: Dict[str, Any] = {
        'day_length': day_length,
        'max_work_day': max_work_day,
        'rest_type': rest_type,
        'night_type': night_type,
        'work_type_time': work_type_time,
        'shift_pattern_dict': shift_pattern_dict,
        'rest_requests': rest_requests,
        'shift_pattern': shift_pattern,
    }

    shift_config: ShiftConfig = ShiftConfig(**params)
    genom_shift_manager: GenomShiftManager = GenomShiftManager(shift_config)

    best: GenomShift = genom_shift_manager.execute()

    end_time: float = time.time() - start_time
    h_shift: List[List[int]] = best.get_h_shift()
    loss: float = best.get_loss()
    error_line: List[Set[int]] = best.get_error_line()
    total_work_time_avg: float = best.get_total_work_time_avg()
    total_work_time_list: List[float] = best.get_total_work_time_list()
    rest_requests = genom_shift_manager.get_shift_config().get_rest_requests()
    shift_pattern = genom_shift_manager.get_shift_config().get_shift_pattern()
    shift_pattern_dict = genom_shift_manager.get_shift_config().get_shift_pattern_dict()
    print(f'--------------------------------------')

    # 処理時間
    print(f'Time(s): {end_time}')

    # 総合評価
    print(f'Loss: {loss}')

    # 平均勤務時間
    print(f'Work Time Avg: {total_work_time_avg}')

    # 希望休
    print(f'Rest Requests:')
    for rest in rest_requests:
        print(f'{rest}')

    # シフトパターン内容
    print(f'Sfhit Pattern:')
    for key, val in shift_pattern_dict.items():
        print(f'{key}: {val}')

    # 欠陥箇所
    print(f'Errors:')
    for i, error in enumerate(error_line):
        print(f'{i}: {sorted(error) if len(error) > 0 else "OK"}')

    # 完成シフトをコンソールに表示
    print(' - ' + ' '.join([str(i).rjust(2) for i in range(day_length)]))
    for i, shift in enumerate(h_shift):
        line = f'{str(i).rjust(2)} '
        for j, s in enumerate(shift):
            if j in error_line[i]:
                line += str(Color.RED + str(s).rjust(2) + Color.END + ' ')
            elif j in rest_requests[i]:
                line += str(Color.GREEN + str(s).rjust(2) + Color.END + ' ')
            else:
                line += str(str(s).rjust(2) + ' ')
        print(f'{line} {total_work_time_list[i]}')

    # シフトパターン
    print('   ' + ' '.join([str(i).rjust(2) for i in shift_pattern]))
