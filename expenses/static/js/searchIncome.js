const searchField=document.querySelector('#searchField');
const myChart=document.querySelector('#myChart');
const tableOutput=document.querySelector('.table_output');
const appTable=document.querySelector('.app_table');
const paginationContainer=document.querySelector('.pagination_container');
const searchTableBody=document.querySelector('.search_table_body');
const noResult=document.querySelector('.no_result');
const delay_by_in_ms = 700;

console.log('test seach expense')
tableOutput.style.display="none";
noResult.style.display="none";
searchField.addEventListener('keyup',(e)=>{
    const searchValue=e.target.value;
    if(searchValue.trim().length>0){
        paginationContainer.style.display="none";
        myChart.style.display="none";
        searchTableBody.innerHTML="";
        noResult.style.display="none";
        fetch("/search_incomes",{
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data', data);
            appTable.style.display="none";
            tableOutput.style.display="block";

            if(data.length===0){
                tableOutput.style.display="none";
                noResult.style.display="block";
            }else{
                data.forEach((item)=>{
                searchTableBody.innerHTML +=`
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
                });
            }
        });
    }else{
        myChart.style.display="block";
        appTable.style.display="block";
        paginationContainer.style.display="block";
        tableOutput.style.display="none";
    }

});