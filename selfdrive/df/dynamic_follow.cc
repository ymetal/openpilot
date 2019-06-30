#include "dynamic_follow.h"

std::unique_ptr<zdl::SNPE::SNPE> snpe;

float *output;

zdl::DlSystem::Runtime_t checkRuntime()
{
    static zdl::DlSystem::Version_t Version = zdl::SNPE::SNPEFactory::getLibraryVersion();
    static zdl::DlSystem::Runtime_t Runtime;
    std::cout << "SNPE Version: " << Version.asString().c_str() << std::endl; //Print Version number
    if (zdl::SNPE::SNPEFactory::isRuntimeAvailable(zdl::DlSystem::Runtime_t::GPU)) {
        Runtime = zdl::DlSystem::Runtime_t::GPU;
    } else {
        Runtime = zdl::DlSystem::Runtime_t::CPU;
    }
    return Runtime;
}

void initializeSNPE(zdl::DlSystem::Runtime_t runtime) {
  std::unique_ptr<zdl::DlContainer::IDlContainer> container;
  container = zdl::DlContainer::IDlContainer::open("/data/openpilot/selfdrive/df/LSTM.dlc");
  //printf("loaded model\n");
  int counter = 0;
  zdl::SNPE::SNPEBuilder snpeBuilder(container.get());
  snpe = snpeBuilder.setOutputLayers({})
                      .setRuntimeProcessor(runtime)
                      .setUseUserSuppliedBuffers(false)
                      .setPerformanceProfile(zdl::DlSystem::PerformanceProfile_t::HIGH_PERFORMANCE)
                      .build();
}



std::unique_ptr<zdl::DlSystem::ITensor> loadInputTensor(std::unique_ptr<zdl::SNPE::SNPE> &snpe, std::vector<float> inputVec) {
  std::unique_ptr<zdl::DlSystem::ITensor> input;
  const auto &strList_opt = snpe->getInputTensorNames();
  if (!strList_opt) throw std::runtime_error("Error obtaining Input tensor names");
  const auto &strList = *strList_opt;

  const auto &inputDims_opt = snpe->getInputDimensions(strList.at(0));
  const auto &inputShape = *inputDims_opt;

  input = zdl::SNPE::SNPEFactory::getTensorFactory().createTensor(inputShape);
  std::copy(inputVec.begin(), inputVec.end(), input->begin());

  return input;
}

float returnOutput(const zdl::DlSystem::ITensor* tensor) {
  float op = *tensor->cbegin();
  return op;
}

zdl::DlSystem::ITensor* executeNetwork(std::unique_ptr<zdl::SNPE::SNPE>& snpe,
                    std::unique_ptr<zdl::DlSystem::ITensor>& input) {
  static zdl::DlSystem::TensorMap outputTensorMap;
  snpe->execute(input.get(), outputTensorMap);
  zdl::DlSystem::StringList tensorNames = outputTensorMap.getTensorNames();

  const char* name = tensorNames.at(0);  // only should the first
  auto tensorPtr = outputTensorMap.getTensor(name);
  return tensorPtr;
}

extern "C" {
  float run_model(float v_ego, float a_ego, float v_lead, float x_lead, float a_lead){
    std::vector<float> inputVec;
    float b = 10;
    for (int i = 0; i < b; i++) {
      inputVec.push_back(8.9408);
      inputVec.push_back(0);
      inputVec.push_back(8.9);
      inputVec.push_back(15);
      inputVec.push_back(0);
    }
    for (int i = 0; i < b; i++) {
      inputVec.push_back(8.9408);
      inputVec.push_back(0);
      inputVec.push_back(12);
      inputVec.push_back(23);
      inputVec.push_back(.2);
    }

    std::unique_ptr<zdl::DlSystem::ITensor> inputTensor = loadInputTensor(snpe, inputVec);
    zdl::DlSystem::ITensor* oTensor = executeNetwork(snpe, inputTensor);
    return returnOutput(oTensor);
  }

  void init_model(){
    zdl::DlSystem::Runtime_t runt=checkRuntime();
    initializeSNPE(runt);
  }

  void test_input(float inputArray[20][5]){
    std::cout << "hello!\n";

    /*std::vector<std::vector<float>> inputVec;

    std::vector<float> v(inputArray[0], inputArray[0] + sizeof inputArray[0] / sizeof inputArray[0][0]);
    inputVec.push_back(v);
    inputVec.push_back(v);

    std::unique_ptr<zdl::DlSystem::ITensor> inputTensor = loadInputTensor(snpe, inputVec);
    zdl::DlSystem::ITensor* oTensor = executeNetwork(snpe, inputTensor);
    std::cout << returnOutput(oTensor);*/
  }

  int main(){
    std::cout << "hello";
    return 0;
  }

}
