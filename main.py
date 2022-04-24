import backpack_problem
import as_foa



if __name__ == "__main__":
    problems = backpack_problem.read_backpack_problems()
    for problem in problems:
        print(as_foa.as_foa_for_backpack(1000,0.1,100,problem))