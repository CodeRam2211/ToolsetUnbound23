



if(location.href == "http://127.0.0.1:5500/Pages/index.html"){
    const login = document.querySelector(".in-btn")
    login.addEventListener("click", ()=>{
        location.replace("/Pages/dashboard.html")
    })
}

if(location.href == "http://127.0.0.1:5500/Pages/dashboard.html"){
    const signout = document.querySelector(".lout")
    const logo = document.querySelector(".logo")
    const myFiles = document.querySelector(".my-files")
    signout.addEventListener("click", ()=>{
        console.log("Clicked")
        location.replace("/Pages/index.html")
    })
    logo.addEventListener("click", ()=>{
        console.log("Clicked")
        location.reload()
    })
}
