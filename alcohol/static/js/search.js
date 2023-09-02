function handleEnterKey(event) {
    if (event.key === "Enter") {
      performSearch();
    }
  }
  
function performSearch() {
    var input = document.getElementById('searchInput').value.trim().toLowerCase();
    var selectedOption = document.getElementById('searchOption').value;
    var alcoholItems = document.getElementsByClassName('alcohol-item');
  
    if (input === '') {
        for (var i = 0; i < alcoholItems.length; i++) {
            alcoholItems[i].style.display = 'block';
        }
        return;
    }
  
    for (var i = 0; i < alcoholItems.length; i++) {
        var itemText = alcoholItems[i].innerText.toLowerCase();
        var optionText = '';

        if (selectedOption === 'all') {
            optionText = itemText;
        } else {
            optionText = alcoholItems[i].getElementsByClassName(selectedOption)[0].nextSibling.nodeValue.trim().toLowerCase();
        }

        if (optionText.includes(input)) {
            alcoholItems[i].style.display = 'block';
        } else {
            alcoholItems[i].style.display = 'none';
        }
    }
}

