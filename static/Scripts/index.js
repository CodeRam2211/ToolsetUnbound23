const signup = document.querySelector(".sign-btn");
const create = document.querySelector(".su-btn")
signup.addEventListener("click", ()=>{
    const forms = document.querySelectorAll(".login");
    forms.forEach((e)=>{
        if(e.classList.contains("hidden")){
            e.classList.remove("hidden");
        }
        else{
            e.classList.add("hidden")
        }
    })
});
create.addEventListener("click", ()=>{

    const forms = document.querySelectorAll(".login");
    forms.forEach((e)=>{
        if(e.classList.contains("hidden")){
            e.classList.remove("hidden");
        }
        else{
            e.classList.add("hidden")
        }
    })
});