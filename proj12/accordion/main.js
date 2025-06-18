const data = [
  {
    id : '1',
    q: "what are you",
    a: "reader"
  },
  {
    id: '2',
    q: "what do you do?",
    a: "read"
  },
  {
    id : '3',
    q: "what do u read?",
    a: "everything"
  },
] ;
const accordionWrapper = document.querySelector('.accordion');

function createAccordion() {
accordionWrapper.innerHTML = data.map(dataItem=> <div class="accordion_item"> 
<div> </div>
</div>)
}
createAccordion();