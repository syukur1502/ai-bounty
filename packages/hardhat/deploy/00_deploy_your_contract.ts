import { HardhatRuntimeEnvironment } from "hardhat/types";
import { DeployFunction } from "hardhat-deploy/types";

const deployYourContract: DeployFunction = async function (hre: HardhatRuntimeEnvironment) {
  const { deployer } = await hre.getNamedAccounts();
  const { deploy } = hre.deployments;

  await deploy("YourContract", {
    from: deployer,
    // Args harus kosong karena constructor kita tidak butuh input
    args: [],
    log: true,
    autoMine: true,
  });
};

export default deployYourContract;
deployYourContract.tags = ["YourContract"];
