

import matplotlib.pyplot as plt




blue = '#3752a4'
green = '#22a831'
perp  = '#C6B3D3'
deepbule  = '#797BB7'
red = '#eb1d22'
yellow = '#ff9900'

if __name__ == "__main__":

    val_list = []
    val_list_time_notopK = []

    file_path = "/home/wy/semSLAM/rangetnet_pp/src/time.txt"
    file_path_time_notopK = "/home/wy/semSLAM/rangetnet_pp/src/time_notopK.txt"
    with open(file_path, 'r') as f:
        for line in f:
            val = line.split()
            val_list.append(float(val[0]))

    with open(file_path_time_notopK, 'r') as f:
        for line in f:
            val = line.split()
            val_list_time_notopK.append(float(val[0]))
    # print(val_list)




    execution_times = val_list
    average_execution_time = sum(execution_times) / len(execution_times)
    average_execution_time_notopK = sum(val_list_time_notopK) / len(val_list_time_notopK)

    plt.figure(figsize=(8, 6))
    plt.plot(execution_times, color= red, marker='.', linestyle='-', label='average_execution_time_withTopK')
    plt.plot(val_list_time_notopK, color= blue, marker='.', linestyle='-', label='average_execution_time_withoutTopK')

    # plt.axhline(y=average_execution_time, color=red, linestyle='--', label='average_execution_time_withTopK')
    # plt.text(len(execution_times) * 0.4, average_execution_time * 1.05, 
    #     'average_execution_time_withTopK: {:.2f} ms'.format(average_execution_time), 
    #     color=red,fontsize=14)


    # plt.axhline(y=average_execution_time_notopK, color=yellow, linestyle='--', label='average_execution_time_withoutTopK')
    # plt.text(len(average_execution_time_notopK) * 0.4, average_execution_time_notopK * 1.05, 
    #     'average_execution_time_withoutTopK: {:.2f} ms'.format(average_execution_time_notopK), 
    #     color=yellow,fontsize=14)

    plt.xlabel('lidar point Index', fontsize=12)
    plt.ylabel('Execution Time (milliseconds)', fontsize=12)
    plt.title('Execution Time for Each lidar point', fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.ylim(16, 22)

    # plt.show()
    plt.savefig("timecompare.png",dpi=600, bbox_inches='tight')

    improvement_percentage = (abs((average_execution_time_notopK - average_execution_time)) / average_execution_time_notopK) * 100

    print(f"Average execution time improvement is {improvement_percentage:.2f}%")
    print(f"average_execution_time {average_execution_time:.2f}ms")
    print(f"average_execution_time_notopK {average_execution_time_notopK:.2f}ms")