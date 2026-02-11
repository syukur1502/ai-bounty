// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;

contract YourContract {

    struct Task {
        uint256 id;
        string description;
        uint256 reward;
        bool isCompleted;
        address completedBy;
        string result; // <--- KOLOM BARU: Tempat Jawaban AI
    }

    mapping(uint256 => Task) public tasks;
    uint256 public taskCount = 0;

    event TaskCreated(uint256 id, string description, uint256 reward);
    event TaskCompleted(uint256 id, address agent, string result); // Event juga diupdate

    function postTask(string memory _description) public payable {
        require(msg.value > 0, "Reward harus lebih dari 0!");
        
        taskCount++;
        tasks[taskCount] = Task(
            taskCount,
            _description,
            msg.value,
            false,
            address(0),
            "" // Awalnya jawaban kosong
        );

        emit TaskCreated(taskCount, _description, msg.value);
    }

    // Fungsi ini kita update supaya Agent bisa setor jawaban (_result)
    function completeTask(uint256 _taskId, string memory _result) public {
        Task storage task = tasks[_taskId];

        require(task.id != 0, "Tugas tidak ditemukan!");
        require(!task.isCompleted, "Tugas sudah selesai bos!");

        task.isCompleted = true;
        task.completedBy = msg.sender;
        task.result = _result; // Simpan jawaban AI ke Blockchain

        (bool success, ) = payable(msg.sender).call{value: task.reward}("");
        require(success, "Gagal transfer uang");

        emit TaskCompleted(_taskId, msg.sender, _result);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}