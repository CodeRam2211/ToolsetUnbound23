const btn = document.querySelector(".upload");

btn.addEventListener("click", (e)=>{
    const upbox = document.querySelector(".up-box");
    const compdis = document.querySelector(".comp-dis");
    compdis.classList.remove("hidden")
    upbox.classList.add("hidden")
})

const again = document.getElementById("comp-again")
again.addEventListener("click", ()=>{
    const upbox = document.querySelector(".up-box");
    const compdis = document.querySelector(".comp-dis");
    upbox.classList.remove("hidden")
    compdis.classList.add("hidden");
})