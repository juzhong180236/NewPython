# """
# Code that goes along with the Airflow tutorial located at:
# https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
# """
# from airflow import DAG
# from airflow.operators.bash_operator import BashOperator
# from datetime import datetime, timedelta
import numpy as np


# default_args = {
#     'owner': 'Airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2015, 6, 1),
#     'email': ['airflow@example.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
#     # 'queue': 'bash_queue',
#     # 'pool': 'backfill',
#     # 'priority_weight': 10,
#     # 'end_date': datetime(2016, 1, 1),
# }
#
# dag = DAG('tutorial', default_args=default_args, schedule_interval=timedelta(days=1))
#
# # t1, t2 and t3 are examples of tasks created by instantiating operators
# t1 = BashOperator(
#     task_id='print_date',
#     bash_command='date',
#     dag=dag)
#
# t2 = BashOperator(
#     task_id='sleep',
#     bash_command='sleep 5',
#     retries=3,
#     dag=dag)
#
# templated_command = """
#     {% for i in range(5) %}
#         echo "{{ ds }}"
#         echo "{{ macros.ds_add(ds, 7)}}"
#         echo "{{ params.my_param }}"
#     {% endfor %}
# """
#
# t3 = BashOperator(
#     task_id='templated',
#     bash_command=templated_command,
#     params={'my_param': 'Parameter I passed in'},
#     dag=dag)
#
# t2.set_upstream(t1)
# t3.set_upstream(t1)

# if np.nan > 0:
# print(np.where(np.array([1, 4, 5, 6, 0, 5])))
# print(np.nan > 0)
def de(a):
    a.append(1)


# print('abaa'.rstrip('a'))
a = [1, 2, 3.4, 4]
# print(','.join(map(str, a)))
de(a)
print(a)

