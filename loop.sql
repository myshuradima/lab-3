set SERVEROUTPUT ON
declare 
    v_genre_id genres.genre_id%type := 0;
    v_genre_name genres.genre%type := 'Genre';
    v_string VARCHAR2(20);
begin
    for i in 1..100
    loop
        v_genre_id := i;
        v_string := to_char(i);
        v_genre_name := 'Genre' || v_string;
        DBMS_OUTPUT.PUT_LINE(v_genre_name);
        insert into genres(genre_id, genre) values (v_genre_id, v_genre_name);
    end loop;
end;
