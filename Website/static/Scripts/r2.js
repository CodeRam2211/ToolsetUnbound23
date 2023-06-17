



if(location.href == "http://127.0.0.1:5000/"){
    const login = document.querySelector(".in-btn")
    login.addEventListener("click", ()=>{
        location.replace("/login")
    })
}

if(location.href != "http://127.0.0.1:5000"){
    const signout = document.querySelector(".lout")
    const logo = document.querySelector(".logo")
    const myFiles = document.querySelector("#files")
    const comp = document.querySelector(".compress")
    signout.addEventListener("click", ()=>{
        location.replace("/")
    })
    logo.addEventListener("click", ()=>{
        location.replace("/dashboard")
    })

    myFiles.addEventListener("click", ()=>{
        location.replace("/files")
    })
    comp.addEventListener("click", ()=>{
    })
}
