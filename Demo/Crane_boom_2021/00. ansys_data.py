from ansys.dpf import post
from ansys.dpf.post import examples

path_read = r"D:\Alai\ansys_Alai\Crane\Crane_Parts_v2.0\truss_low_fidelity_20210629_150\20191220_files\dp0\SYS-14\MECH"

solution = post.load_solution(path_read + r'\file.rst')
# result_info = solution.get_result_info()
# print(result_info)
print(solution.mesh)
displacement = solution.displacement()
u_y = displacement.y
print(len(u_y.get_data_at_field()))
stress = solution.stress()
print()

