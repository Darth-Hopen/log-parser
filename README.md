# log-parser

Описание/Пошаговая инструкция выполнения домашнего задания:
Написать скрипт анализа приложенного access.log файла
Ссылка на файл access.log приложена в материалах к занятию
Формат записи в файле лога:
%h %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i" %D
%h - имя удаленного хоста
%t - время получения запроса
%r - тип запроса, его содержимое и версия
%s - код состояния HTTP
%b - количество отданных сервером байт
%{Referer} - URL-источник запроса
%{User-Agent} - HTTP-заголовок, содержащий информацию о запросе
%D - длительность запроса в миллисекундах

Скрипт запускается командой log_parser.py - <путь до файла/директории>

