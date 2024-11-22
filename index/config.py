import time

cd=4.9
iptime_g_each=1
iptime_g=4.4
iptime_g_a_each=1
iptime_g_a=2.9
iptime_a_each=80
iptime_a=0.9
save_to_db_cd=10.0
need_to_save_as_file=0
roottext="PBD-HPD-0HzIr-LCsy"
root=[710036, 378849]
start_time = time.mktime(time.strptime("Jun 30 00:00:00 2024","%b %d %H:%M:%S %Y"))
end_time = time.mktime(time.strptime("Aug 30 23:59:59 2024","%b %d %H:%M:%S %Y"))
upd_from_server = 0.1


url = "https://api.paintboard.ayakacraft.com:11451/api/paintboard/"
board = "getboard"