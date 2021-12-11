
if (localStorage["clicked"]) {
    console.log(true);
    document.getElementById('cookie-banner').classList.add('visually-hidden')
}else{
    let cookieBtn = document.getElementById("cookie");
    if(cookieBtn){
    cookieBtn.addEventListener('click',function(){
    document.getElementById('cookie-banner').classList.add('visually-hidden')
    localStorage.setItem("clicked","clicked")
   })
  }
}

let spinner = document.getElementById('spinner');
    let form = document.getElementById('form-head');
    let searchButton = document.getElementById('button-addon2');
    let input = document.getElementById('input');


    
    //disable button if its empty
    if(input){
      input.addEventListener("input", buttonFunc);
      function buttonFunc(e) {
     if(input.value.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+~#?&/=]*)/g) && input.value.includes('github.com') && input.value.length != 0 ) {
        searchButton.disabled = false
      } else{
        searchButton.disabled = true
      }
     }
    }
    // onclick hide the form and show spinner
    if(searchButton){
    searchButton.addEventListener('click',function(e){
    spinner.classList.remove('visually-hidden');
    form.classList.add('visually-hidden');
    totalSeconds = 0;
    countTimer()
     })
   }
   // generate pdf
   let pdfButton = document.getElementById("pdf");
   if(pdfButton){
    pdfButton.onclick= function(){

      
      let results = document.getElementById("response_table");

       document.getElementById("table").classList.add('bg-dark');
       
       let opt = {
         margin: 1,
         filename: `${a.name}_dependencies.pdf`,
         image: { type: 'jpeg', quality: 0.98 },
         html2canvas: { scale: 2 },
         jsPDF:  { unit: 'in', format:'letter', orientation: 'portrait'}
       };
       html2pdf(results, opt)
      }
   }

   
   
   
   var timerVar = setInterval(countTimer, 1000);
   var totalSeconds = 0;
   function countTimer() {
           ++totalSeconds;
           var hour = Math.floor(totalSeconds /3600);
           var minute = Math.floor((totalSeconds - hour*3600)/60);
           var seconds = totalSeconds - (hour*3600 + minute*60);
           
           if(minute < 10)
             minute = "0"+minute;
           if(seconds < 10)
             seconds = "0"+seconds;
             if(spinner.classList.contains('visually-hidden')){
             document.getElementById("timer").innerHTML = ''
             }else{
           document.getElementById("timer").innerHTML ='Scanning the repo for '+  minute + ":" + seconds + ' seconds';
             }
        }
        let todayDate = document.getElementById("today-date")
        if(todayDate){
        var today = new Date();
        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        todayDate.innerHTML ='Today date: ' + date
        }

      


