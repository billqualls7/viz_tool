#include "netTensorRT.hpp"
#include "pointcloud_io.h"
#include "yaml-cpp/yaml.h"
#include <filesystem>
#include <iostream>
#include <string>
#include <sys/resource.h>
#include <nvml.h>


void inline initialGPU() {
  cudaSetDevice(0);
  cudaFree(0);
}

int main(int argc, const char *argv[]) {
  // step1: initial the GPU
  initialGPU();

  // step2: get the config parameters
  std::filesystem::path file_path(__FILE__);
  auto config_path = std::string(file_path.parent_path().parent_path() / "config" / "infer.yaml");

  YAML::Node config = YAML::LoadFile(config_path);
  std::string data_path = std::string(file_path.parent_path().parent_path()) + "/" + config["DATA_PATH"].as<std::string>();
  const std::string model_dir = std::string(file_path.parent_path().parent_path() / "model/");

  // step3: load the pointcloud
  pcl::PointCloud<PointType>::Ptr pointcloud(new pcl::PointCloud<PointType>);
  std::cout << "loading file: " << data_path << std::endl;
  if (pcl::io::loadPCDFile<PointType>(data_path, *pointcloud) == -1) {
    PCL_ERROR("Couldn't read file \n");
    exit(EXIT_FAILURE);
  }

  // step4: create the engine
  namespace cl = rangenet::segmentation;
  auto net = std::unique_ptr<cl::Net>(new cl::NetTensorRT(model_dir, false));

  // step5: infer
  cv::TickMeter tm;
  struct rusage usage;



  nvmlReturn_t result;
  unsigned int deviceCount=0;
   // 可以修改为获取特定GPU的句柄

  // 初始化NVML
  result = nvmlInit();

  result = nvmlDeviceGetCount(&deviceCount);
  
  if (NVML_SUCCESS != result)
    {
        std::cout << "Failed to query device count: " << nvmlErrorString(result);
    }
    std::cout << "Found:" << deviceCount <<" device" << endl;


  nvmlDevice_t device ;
  result = nvmlDeviceGetHandleByIndex(0, &device);


  


  for (int i = 0; i < 100; i++) {
    tm.reset();
    tm.start();
    auto labels = std::make_unique<int[]>(pointcloud->size());
    net->doInfer(*pointcloud, labels.get());

    tm.stop();
    auto infer_time = tm.getTimeMilli();
    // std::cout  << infer_time <<  std::endl;
    getrusage(RUSAGE_SELF, &usage);
    double memory_usage_mb = static_cast<double>(usage.ru_maxrss) / 1024;
    //  std::cout << "Memory usage: " << std::fixed << std::setprecision(2) << memory_usage_mb << " MB" << std::endl;
    // std::cout << memory_usage_mb << std::endl;
    // std::cout << "infer time: " << infer_time << " ms." << std::endl;
    
    nvmlMemory_t memInfo;
    nvmlUtilization_t utilization;
    result = nvmlDeviceGetMemoryInfo(device, &memInfo);


    result = nvmlDeviceGetUtilizationRates(device, &utilization);


    if (NVML_SUCCESS != result) {
            std::cerr << "Failed to get memory info: " << nvmlErrorString(result) << std::endl;
            continue;
        }
    double free_memory_mb = static_cast<double>(memInfo.free) / (1024 * 1024);
    double used_memory_mb = static_cast<double>(memInfo.used) / (1024 * 1024);
    std::cout 
          << utilization.gpu << "% "
          << used_memory_mb 
          
          << std::endl;
    // system("top -b -n 1 | head -n 6");



  }
  return 0;
}
