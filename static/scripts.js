$(document).ready(()=>{
    document.querySelector('#poleTxt').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      window.location.replace('../' + $("#poleTxt").val())
    }
});
});