const tasklist = document.getElementById("tasklist")
const inputtask = document.getElementById("inputtask")

document.addEventListener("DOMContentLoaded", loadTasks)

function addtasks(){
  const tasktext = inputtask.trim();
  if (tasktext === "") return;
  const task = {id: Date.now(), text: tasktext};
}