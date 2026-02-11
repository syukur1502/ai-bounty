"use client";

import { useState } from "react";
import type { NextPage } from "next";
import { parseEther } from "viem";
import { useScaffoldReadContract, useScaffoldWriteContract } from "~~/hooks/scaffold-eth";

const Home: NextPage = () => {
  // 1. State untuk menyimpan inputan user
  const [taskDescription, setTaskDescription] = useState("");
  const [ethAmount, setEthAmount] = useState("0.001");

  // 2. Fungsi untuk MEMBACA data total tugas (taskCount) dari Blockchain
  const { data: taskCount } = useScaffoldReadContract({
    contractName: "YourContract",
    functionName: "taskCount",
  });

  // 3. Fungsi untuk MEMBACA tugas terakhir
  const { data: lastTask } = useScaffoldReadContract({
    contractName: "YourContract",
    functionName: "tasks",
    args: [taskCount ? taskCount : 0n], // Ambil tugas nomer terakhir
  });

  // 4. Fungsi untuk MENGIRIM tugas (Write Contract)
  const { writeContractAsync: postTask } = useScaffoldWriteContract("YourContract");

  const handleSendTask = async () => {
    try {
      await postTask({
        functionName: "postTask",
        args: [taskDescription],
        value: parseEther(ethAmount),
      });
      alert("Tugas berhasil dikirim ke Blockchain!");
    } catch (e) {
      console.error(e);
      alert("Gagal kirim tugas (Cek Console)");
    }
  };

  return (
    <div className="flex items-center flex-col flex-grow pt-10">
      <div className="px-5">
        <h1 className="text-center mb-8">
          <span className="block text-4xl font-bold">🤖 AI Bounty Dashboard</span>
          <span className="block text-xl mt-2">Perintahkan Robot, Bayar pakai Kripto</span>
        </h1>

        {/* --- KOTAK INPUT TUGAS --- */}
        <div className="bg-base-100 shadow-lg rounded-3xl p-6 mb-10 w-full max-w-lg border-2 border-primary">
          <h2 className="text-2xl font-bold mb-4">✍️ Buat Tugas Baru</h2>

          <label className="label">
            <span className="label-text">Perintah untuk Robot:</span>
          </label>
          <input
            type="text"
            placeholder="Contoh: Cek harga Bitcoin..."
            className="input input-bordered w-full mb-4"
            value={taskDescription}
            onChange={e => setTaskDescription(e.target.value)}
          />

          <label className="label">
            <span className="label-text">Upah (ETH):</span>
          </label>
          <input
            type="number"
            className="input input-bordered w-full mb-4"
            value={ethAmount}
            onChange={e => setEthAmount(e.target.value)}
          />

          <button className="btn btn-primary w-full text-lg" onClick={handleSendTask}>
            🚀 Kirim Tugas
          </button>
        </div>

        {/* --- KOTAK HASIL TUGAS TERAKHIR --- */}
        <div className="bg-base-200 shadow-md rounded-3xl p-6 w-full max-w-lg">
          <h2 className="text-xl font-bold mb-2">📡 Status Tugas Terakhir (ID: {taskCount?.toString()})</h2>

          {lastTask ? (
            <div className="text-left space-y-2">
              <p>
                <strong>📝 Soal:</strong> {lastTask[1]}
              </p>
              <p>
                <strong>⚙️ Status:</strong>{" "}
                {lastTask[3] ? (
                  <span className="text-green-600 font-bold">SELESAI ✅</span>
                ) : (
                  <span className="text-yellow-600 font-bold text-lg animate-pulse">SEDANG DIKERJAKAN ROBOT... ⏳</span>
                )}
              </p>

              {/* Tampilkan Jawaban jika sudah selesai */}
              {lastTask[3] && (
                <div className="mt-4 p-4 bg-white rounded-xl border border-gray-300">
                  <p className="font-bold text-primary">💡 Jawaban Robot:</p>
                  <p className="text-lg">{lastTask[5]}</p>
                </div>
              )}
            </div>
          ) : (
            <p>Belum ada tugas.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
