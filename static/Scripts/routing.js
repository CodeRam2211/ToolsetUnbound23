



if(location.href == "http://127.0.0.1:5000/"){
    const login = document.querySelector(".in-btn")
    login.addEventListener("click", ()=>{
        location.replace("/dashboard")
    })
}

if(location.href == "http://127.0.0.1:5000/dashboard"){
    const signout = document.querySelector(".lout")
    const logo = document.querySelector(".logo")
    const myFiles = document.querySelector(".my-files")
    signout.addEventListener("click", ()=>{
        console.log("Clicked")
        location.replace("/")
    })
    logo.addEventListener("click", ()=>{
        console.log("Clicked")
        location.reload()
    })
}
