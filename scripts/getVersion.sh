#!/bin/bash

if [ ! $# -eq 0 ]
then
    CURRENT_FILE=`basename $1`
    CURRENT_DIR=`dirname $1`

    OBJ_DUMP_f=/tmp/${CURRENT_FILE}_objdump.tmp
    #HEX_DUMP_f=/tmp/${CURRENT_FILE}_hexdump.tmp
    READ_ONLY_f=/tmp/${CURRENT_FILE}_readonly.tmp

    objdump -t ${CURRENT_DIR}/${CURRENT_FILE} > $OBJ_DUMP_f
    #xxd -e ${CURRENT_FILE} > $HEX_DUMP_f
    objdump -s -j .rodata ${CURRENT_DIR}/${CURRENT_FILE} > $READ_ONLY_f

    # Define how the output shall be formatted.
    FORMAT_OUTPUT=1

    # Define the order and the flags that shall be processed.
    VERSION_INFO="VERSION_MAJOR\
                  VERSION_MINOR\
                  VERSION_PATCH\
                  VERSION_REVISION\
                  IS_DEBUG\
                  BUILD_NUMBER\
                  BUILD_DAY\
                  BUILD_MONTH\
                  BUILD_YEAR\
                  BUILD_HOUR\
                  BUILD_MINUTE\
                  BUILD_SECOND"
fi

if [ $# -eq 1 ]
then
    # remove file extention of the first argument
    COMPONENTS=$(echo ${CURRENT_FILE} | sed -nr "s/(.*)\..*/\1/p")

    if [[ -z $COMPONENTS ]]
    then
        COMPONENTS=${CURRENT_FILE}
    fi

    echo No second argument specified, searching for all entries.
    COMPONENTS=`cat $OBJ_DUMP_f | grep REF | sed -nre 's/.*JVersion[0-9]*(.*)[0-9]{2,}BUILD_NUMBER_REF.*/\1/p'`

elif [ $# -eq 2 ]
then
    # remove file extention of second argument
    COMPONENTS=$(echo $2 | sed -nr "s/(.*)\..*/\1/p")
    if [[ -z $COMPONENTS ]]
    then
        COMPONENTS=$2
    fi
else
    echo "  "usage: "   "getVersion.sh fileToSearch
    echo "  "optional: getVersion.sh fileToSearch entryToSearch
    exit
fi

for c in $COMPONENTS
do
    echo "  Version information of component: "$c
    WAS_DEBUG=0
    for v in $VERSION_INFO
    do
        SYMBOLS=`cat $OBJ_DUMP_f | sed -nre "s/([0-9 a-f]*).*\.rodata.*JVersion[0-9]*${c}[0-9]*${v}_REF.*/\1/p"`
        for s in $SYMBOLS
        do
            # echo searching value for Symbol at adress: $s
            id=`echo $s | rev | cut -c 1`
            id=`perl -le "print hex("${id}");"`
            id=$((id/4 + 1))
            catSym=`echo $s | rev | cut -c 2-4 | rev`
            # echo $catSym, id = $id
            #line=`cat $HEX_DUMP_f | sed -nre "s/${catSym}0:\s*([0-9 a-f]*)\s*([0-9 a-f]*)\s*([0-9 a-f]*)\s*([0-9 a-f]*).*/\1 \2 \3 \4/p"`
            line=`cat $READ_ONLY_f | sed -nre "s/\s*${catSym}0\s*([0-9 a-f]*)\s*([0-9 a-f]*)\s*([0-9 a-f]*)\s*([0-9 a-f]*).*/\1 \2 \3 \4/p"`
            value=`echo $line | cut -d " " -f $id`
            value=`echo ${value:6:2}${value:4:2}${value:2:2}${value:0:2}`
            # echo $value
            if [[ $value ]]; then
                if [ $FORMAT_OUTPUT -eq 0 ]; then
                    printf "    %-17s: %6d\n" $v 0x$value
                else
                    case "$v" in
                        VERSION_MAJOR)
                            printf "    v%d" 0x$value
                            ;;

                        VERSION_MINOR|VERSION_PATCH)
                            printf ".%d" 0x$value
                            ;;

                        VERSION_REVISION)
                            printf " Revision: %d\n" 0x$value
                            ;;

                        IS_DEBUG)
                            WAS_DEBUG=1
                            if [ $value -eq 1 ]; then
                                printf "    Debug b"
                            else
                                printf "    Release b"
                            fi
                            ;;

                        BUILD_NUMBER)
                            if [ $WAS_DEBUG -eq 0 ]; then printf "    B"; fi
                            printf "uild #%d - " 0x$value
                            ;;

                        BUILD_DAY|BUILD_MONTH)
                            printf "%02d." 0x$value
                            ;;

                        BUILD_YEAR)
                            printf "%04d, " 0x$value
                            ;;

                        BUILD_HOUR|BUILD_MINUTE)
                            printf "%02d:" 0x$value
                            ;;

                        BUILD_SECOND)
                            printf "%02d\n" 0x$value
                            ;;
                    esac
                fi
            fi
        done # SYMBOLS
    done # VERSION_INFO
done # COMPONENTS

# delete temporary files.
rm $OBJ_DUMP_f
#rm $HEX_DUMP_f
rm $READ_ONLY_f
