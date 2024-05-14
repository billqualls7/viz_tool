import matplotlib.pyplot as plt



average_execution_time_topk = 17.98
average_execution_time_notopK = 20.02


blue = '#3752A4'
red = '#eb1d22'


def readgpuinfo(path):
    used_list = []
    gpumemory_list = []

    with open(path, 'r') as f:
        for line in f:
            data = line.strip()
            used, gpumemory = data.split()
            used_list.append(float(used.rstrip('%')))
            gpumemory_list.append(float(gpumemory))
    return used_list, gpumemory_list


def readmemory(path):
    val_list =[]
    with open(path, 'r') as f:
        for line in f:
            val = line.split()
            val_list.append(float(val[0]))

    return val_list


if __name__ == "__main__":
    memorynotok_path = '/home/wy/semSLAM/rangetnet_pp/src/memorynotok.txt'
    memorywithTopk_path = '/home/wy/semSLAM/rangetnet_pp/src/memorywithTopk.txt'
    gpuinfowithTopK_path  = '/home/wy/semSLAM/rangetnet_pp/src/gpuinfowithTopK.txt'
    gpuinfowithoutTopK_path  = '/home/wy/semSLAM/rangetnet_pp/src/gpuinfowithoutTopK.txt'
    

    M_notopk = readmemory(memorynotok_path)
    M_topk = readmemory(memorywithTopk_path)

    average_M_notopk = sum(M_notopk)/len(M_notopk)
    average_M_topk = sum(M_topk)/len(M_topk)


    # print(average_M_notopk)
    # print(average_M_topk)



    GPUused_notopk, GPU_M_notopk = readgpuinfo(gpuinfowithoutTopK_path)
    GPUused_topk, GPU_M_topk = readgpuinfo(gpuinfowithTopK_path)

    average_GPU_M_notopk = sum(GPU_M_notopk)/len(GPU_M_notopk)
    average_GPU_M_topk = sum(GPU_M_topk)/len(GPU_M_topk)


    average_GPU_used_notopk = sum(GPUused_notopk)/len(GPUused_notopk)
    average_GPU_used_topk = sum(GPUused_topk)/len(GPUused_topk)

    # print(average_GPU_M_notopk)
    # print(average_GPU_M_topk)
    # print(average_GPU_used_notopk)
    # print(average_GPU_used_topk)

    notopk = [average_execution_time_notopK, average_M_notopk, average_GPU_M_notopk, average_GPU_used_notopk]
    topk = [average_execution_time_topk, average_M_topk, average_GPU_M_topk, average_GPU_used_topk]
    print(notopk)
    print(topk)




    # 计算提升百分比
    increase_percentage = [0]  # 初始化为0，避免索引错误
    for d1, d2 in zip(notopk, topk):
        if d1 != 0:  # 防止除以0的情况
            increase_percentage.append((d2 - d1) / d1 * 100)
        else:
            increase_percentage.append(0)
    
    x = range(len(notopk))
    width = 0.35  # 条形的宽度

    # 创建分组柱状图
    plt.bar(x, notopk, width, label='WithoutTopK', color=blue)
    plt.bar([i + width for i in x], topk, width, label='WithTopK', color=red)

    # 添加提升百分比标签
    for i in x:
        plt.text(i + width / 2, max(notopk[i], topk[i]), f'{increase_percentage[i + 1]:.1f}%', ha='center')
    # 添加图例
    plt.legend()

    # 添加标题和轴标签
    plt.title('Comparison of TopK-layer')
    plt.xlabel('')
    plt.ylabel('')
    plt.yscale('log')
    # 设置x轴标记
    plt.xticks([i + width / 2 for i in x], ['Time(ms)', 'Memory(MB)', 'GPUMemory(MB)', 'GPUUsed(%)'])

    # 显示图表
    plt.tight_layout()  # 调整布局以适应标签
    plt.show()