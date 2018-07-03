months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
la_week=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
day_week=["Sun", "Mon","Tue","Wed","Thu","Fri","Sat"];

function calendar(){
    today=new Date();
    day_wc=today.getDay();
    day_c=today.getDate();
    month_c=today.getMonth();
    year_c=today.getFullYear();

    titles=document.getElementById("titles");
    prev=document.getElementById("prev");
    next=document.getElementById("next");

    r0=document.getElementById("row0");
    
    pie=document.getElementById("current_date");
    pie.innerHTML += la_week[day_wc]+", "+day_c+" of "+months[month_c]+", "+year_c;

    document.search.search_year.value=year_c;
    month_cal = month_c;
    year_cal = year_c

    header()
    first_line()
    write_days()
}

function header() {
    titles.innerHTML=months[month_cal]+", "+year_cal;
    month_prev=month_cal-1;
    month_next=month_cal+1;
    if (month_prev<0){
        month_prev=11;
    }
    if (month_next>11){
        month_next=0;
    }

    prev.innerHTML=months[month_prev]
    next.innerHTML=months[month_next]
}

function first_line() {
    for (i=0;i<7;i++) {
        grid0=r0.getElementsByTagName("th")[i];
        grid0.innerHTML=day_week[i]
     }
}

function write_days() {
    f_month=new Date(year_cal,month_cal,"0")
    pr_week=f_month.getDay()

    if (pr_week==-1){
        pr_week=6;
    }

    daypr_month=f_month.getDate()
    prcelda=daypr_month-pr_week;
    begin=f_month.setDate(prcelda)
    day_month=new Date()
    day_month.setTime(begin);
    
    for (i=1;i<7;i++){
        row=document.getElementById("row"+i);
        for (j=0;j<7;j++) {
            my_day=day_month.getDate()
            my_month=day_month.getMonth()
            my_year=day_month.getFullYear()

            grid=row.getElementsByTagName("td")[j];
            grid.innerHTML=my_day;

            grid.style.color="black";
            grid.style.backgroundColor="white";

            if (j==0) {
                grid.style.color="#f11445";
            }

            if (my_month!=month_cal) {
                grid.style.color="#a0babc";
            }

            if (my_month==month_c && my_day==day_c && my_year==year_c ) {
                grid.style.backgroundColor="#f0b19e";
            }
            
            my_day=my_day+1;
            day_month.setDate(my_day);
        }
    }
}

function month_p() {
    new_month=new Date()
    f_month--;
    new_month.setTime(f_month)
    month_cal=new_month.getMonth()
    year_cal=new_month.getFullYear()
    header()
    write_days()
}

//ver mes posterior
function month_n() {
    new_month=new Date()
    time_unix=f_month.getTime()
    time_unix=time_unix+(45*24*60*60*1000)
    new_month.setTime(time_unix)
    month_cal=new_month.getMonth()
    year_cal=new_month.getFullYear()
    header()
    write_days()
}

function update() {
    month_cal=today.getMonth();
    year_cal=today.getFullYear();
    header()
    write_days()
}

// temporal
function my_date() {
    my_year=document.search.search_year.value;
    list_months=document.search.search_month;
    options=list_months.options;
    num=list_months.selectedIndex
    my_month=options[num].value;

    if (isNaN(my_year) || my_year<1) {
        alert("Error: Year must be grater than 0")
    }
    else {
        my_dat=new Date();
        my_dat.setMonth(my_month);
        my_dat.setFullYear(my_year);
        month_cal=my_dat.getMonth();
        year_cal=my_dat.getFullYear();
        header()
        write_days()
    }
}