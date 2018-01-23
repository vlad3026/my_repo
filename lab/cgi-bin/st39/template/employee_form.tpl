<form action="/cgi-bin/lab3.py">
    <input type="hidden" name = "student" value={1} />
    <input type="hidden" name = "id" value={2} />
    <input type="hidden" name = "action" value="save_employee" />
    Name: <input type="text" value="{3}" name="name"><br>
    Position: <input type="text" value="{4}" name="position"><br>
    Salary: <input type="text" value="{5}" name="salary"><br>


    <input type="submit" value="Save"/><br>
    <a href="{0}?student={1}"><---</a><br>

</form>