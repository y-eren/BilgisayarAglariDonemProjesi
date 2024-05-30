#include "ns3/command-line.h"
#include "ns3/constant-position-mobility-model.h"
#include "ns3/end-device-lora-phy.h"
#include "ns3/end-device-lorawan-mac.h"
#include "ns3/gateway-lora-phy.h"
#include "ns3/gateway-lorawan-mac.h"
#include "ns3/log.h"
#include "ns3/lora-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/node-container.h"
#include "ns3/periodic-sender-helper.h"
#include "ns3/position-allocator.h"
#include "ns3/simulator.h"
#include "ns3/core-module.h"
#include "ns3/mobility-module.h"
#include "ns3/ns2-mobility-helper.h"

#include <algorithm>
#include <ctime>
#include <vector>

using namespace ns3;
using namespace lorawan;

NS_LOG_COMPONENT_DEFINE("SimpleLorawanNetworkExample");

std::vector<int> packetsSent(1, 0);
std::vector<int> packetsReceived(1, 0);
std::vector<double> sendTimes;
std::vector<double> receiveTimes;

void OnTransmissionCallback(Ptr<const Packet> packet, uint32_t senderNodeId)
{
    NS_LOG_FUNCTION(packet << senderNodeId);
    packetsSent[0]++;
    sendTimes.push_back(Simulator::Now().GetSeconds());  // Paket gönderim zamanını kaydet
}

void OnPacketReceptionCallback(Ptr<const Packet> packet, uint32_t receiverNodeId)
{
    NS_LOG_FUNCTION(packet << receiverNodeId);
    packetsReceived[0]++;
    receiveTimes.push_back(Simulator::Now().GetSeconds());  // Paket alım zamanını kaydet
}

int main(int argc, char* argv[])
{
    int nDevices = 1411;
    int randX= 0;
    int randY= 0;
    int randZ= 0;
    int appPeriodSeconds = 600;  // One packet every .. seconds
    int simulationTimeSeconds = 3600;  // simulasyon zamanı
    CommandLine cmd(__FILE__);
    cmd.AddValue("appPeriodSeconds","Periyodu Degistir", appPeriodSeconds);
    cmd.AddValue("GatewayX", "Initial X coordinate of the gateway", randX);
    cmd.AddValue("GatewayY", "Initial Y coordinate of the gateway", randY);
    cmd.AddValue("GatewayZ", "Initial Z coordinate of the gateway", randZ);
    cmd.Parse(argc, argv);
    // Create the channel
    NS_LOG_INFO("Creating the channel...");
    Ptr<LogDistancePropagationLossModel> loss = CreateObject<LogDistancePropagationLossModel>();
    loss->SetPathLossExponent(3.76);
    loss->SetReference(1, 7.7);
    Ptr<PropagationDelayModel> delay = CreateObject<ConstantSpeedPropagationDelayModel>();
    Ptr<LoraChannel> channel = CreateObject<LoraChannel>(loss, delay);
    // Create the helpers
    NS_LOG_INFO("Setting up helpers...");
    MobilityHelper mobility;
    Ptr<ListPositionAllocator> allocator = CreateObject<ListPositionAllocator>();
    allocator->Add(Vector(randX, randY, randZ));
    mobility.SetPositionAllocator(allocator);
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    LoraPhyHelper phyHelper = LoraPhyHelper();
    phyHelper.SetChannel(channel);
    LorawanMacHelper macHelper = LorawanMacHelper();
    LoraHelper helper = LoraHelper();
    // Create end devices
    NS_LOG_INFO("Creating the end devices...");
    std::string traceFile = "/home/batuhan/ns-allinone-3.41/ns-3.41/scratch/ns2mobility.tcl";
    Ns2MobilityHelper ns2 = Ns2MobilityHelper(traceFile);
    NodeContainer endDevices;
    endDevices.Create(nDevices);
    ns2.Install();
    phyHelper.SetDeviceType(LoraPhyHelper::ED);
    macHelper.SetDeviceType(LorawanMacHelper::ED_A);
    helper.Install(phyHelper, macHelper, endDevices);
    // Create gateways
    NS_LOG_INFO("Creating the gateway...");
    NodeContainer gateways;
    gateways.Create(1);
    mobility.Install(gateways);
    phyHelper.SetDeviceType(LoraPhyHelper::GW);
    macHelper.SetDeviceType(LorawanMacHelper::GW);
    helper.Install(phyHelper, macHelper, gateways);
    // Install applications in end devices
    PeriodicSenderHelper appHelper = PeriodicSenderHelper();
    appHelper.SetPeriod(Seconds(appPeriodSeconds));
    ApplicationContainer appContainer = appHelper.Install(endDevices);
    // Set Data Rates
    std::vector<int> sfQuantity(1);
    sfQuantity = LorawanMacHelper::SetSpreadingFactorsUp(endDevices, gateways, channel);
    // Install trace sources for packet transmission and reception
    for (auto node = endDevices.Begin(); node != endDevices.End(); ++node)
    {
        (*node)->GetDevice(0)->GetObject<LoraNetDevice>()->GetPhy()->TraceConnectWithoutContext(
            "StartSending",
            MakeCallback(OnTransmissionCallback));
    }

    for (auto node = gateways.Begin(); node != gateways.End(); ++node)
    {
        (*node)->GetDevice(0)->GetObject<LoraNetDevice>()->GetPhy()->TraceConnectWithoutContext(
            "ReceivedPacket",
            MakeCallback(OnPacketReceptionCallback));
    }

    // Simulation
    Simulator::Stop(Seconds(simulationTimeSeconds));
    Simulator::Run();
    Simulator::Destroy();
    // Calculate packet delivery ratio
    NS_LOG_INFO("Calculating performance metrics...");
    float totalPacketsSent = packetsSent[0];
    float totalPacketsReceived = packetsReceived[0];
    float totalPacketsLost = totalPacketsSent - totalPacketsReceived;
    float packet_delivery_rate = (totalPacketsReceived / totalPacketsSent) * 100;
    std::cout << "Periyot: " << appPeriodSeconds << " saniye" << std::endl;
    std::cout << "Gonderilen Paket: " << totalPacketsSent << ", "
              << "Ulasan Paket : " << totalPacketsReceived << ", "
              << "Kaybolan Paket: " << totalPacketsLost << ", "
              << "Packet Delivery Rate:" << packet_delivery_rate << std::endl;

    // Calculate delay
    NS_LOG_INFO("Calculating delay metrics...");
    double totalDelay = 0.0;
    for (size_t i = 0; i < receiveTimes.size(); ++i)
    {
        totalDelay += (receiveTimes[i] - sendTimes[i]);
        //std::cout << "Paket " << i + 1 << " Gecikmesi: " << delay << " saniye" << std::endl;  // Her bir paketin gecikmesini yazdır
    }
    double averageDelay = totalDelay / receiveTimes.size();
    std::cout << "Gecikme: " << totalDelay << " ms" << std::endl;
    std::cout << "Ortalama Gecikme: " << averageDelay << " ms" << std::endl;

    return 0;
}

