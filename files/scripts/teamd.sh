#!/bin/bash

. /usr/local/bin/asic_status.sh

function debug()
{
    /usr/bin/logger $1
    /bin/echo `date` "- $1" >> ${DEBUGLOG}
}

function check_warm_boot()
{
    SYSTEM_WARM_START=`$SONIC_DB_CLI STATE_DB hget "WARM_RESTART_ENABLE_TABLE|system" enable`
    SERVICE_WARM_START=`$SONIC_DB_CLI STATE_DB hget "WARM_RESTART_ENABLE_TABLE|${SERVICE}" enable`
    if [[ x"$SYSTEM_WARM_START" == x"true" ]] || [[ x"$SERVICE_WARM_START" == x"true" ]]; then
        WARM_BOOT="true"
    else
        WARM_BOOT="false"
    fi
}

function validate_restore_count()
{
    if [[ x"$WARM_BOOT" == x"true" ]]; then
        RESTORE_COUNT=`$SONIC_DB_CLI STATE_DB hget "WARM_RESTART_TABLE|${SERVICE}" restore_count`
        # We have to make sure db data has not been flushed.
        if [[ -z "$RESTORE_COUNT" ]]; then
            WARM_BOOT="false"
        fi
    fi
}

function check_fast_boot ()
{
    if [[ $($SONIC_DB_CLI STATE_DB GET "FAST_REBOOT|system") == "1" ]]; then
        FAST_BOOT="true"
    else
        FAST_BOOT="false"
    fi
}

start() {
    debug "Starting ${SERVICE}$DEV service..."

    check_warm_boot
    validate_restore_count

    check_fast_boot

    debug "Warm boot flag: ${SERVICE}$DEV ${WARM_BOOT}."
    debug "Fast boot flag: ${SERVICE}$DEV ${Fast_BOOT}."

    # start service docker
    if ! is_chassis_supervisor; then
        /usr/bin/${SERVICE}.sh start $DEV
        debug "Started ${SERVICE}$DEV service..."
    fi
}

wait() {
    if is_chassis_supervisor; then
        # Check asic status before starting docker
        check_asic_status
        ASIC_STATUS=$?

        # start service docker
        if [[ $ASIC_STATUS == 0 ]]; then
            /usr/bin/${SERVICE}.sh start $DEV
            debug "Started ${SERVICE}$DEV service..."
        fi
    fi

    /usr/bin/${SERVICE}.sh wait $DEV
}

stop() {
    debug "Stopping ${SERVICE}$DEV service..."

    check_warm_boot
    check_fast_boot
    debug "Warm boot flag: ${SERVICE}$DEV ${WARM_BOOT}."
    debug "Fast boot flag: ${SERVICE}$DEV ${FAST_BOOT}."

    if [[ x"$WARM_BOOT" == x"true" ]]; then
        # Send USR1 signal to all teamd instances to stop them
        # It will prepare teamd for warm-reboot
        # Note: We must send USR1 signal before syncd, because it will send the last packet through CPU port
        docker exec -i ${SERVICE}$DEV pkill -USR1 ${SERVICE} > /dev/null || [ $? == 1 ]
    elif [[ x"$FAST_BOOT" == x"true" ]]; then
        # Kill teamd processes inside of teamd container with SIGUSR2 to allow them to send last LACP frames
        # We call `docker kill teamd` to ensure the container stops as quickly as possible,
        # Note: teamd must be killed before syncd, because it will send the last packet through CPU port
        docker exec -i ${SERVICE}$DEV pkill -USR2 ${SERVICE} || [ $? == 1 ]
        while docker exec -i ${SERVICE}$DEV pgrep ${SERVICE} > /dev/null; do
            sleep 0.05
        done
        docker kill ${SERVICE}$DEV  &> /dev/null || debug "Docker ${SERVICE}$DEV is not running ($?) ..."
    fi

    /usr/bin/${SERVICE}.sh stop $DEV
    debug "Stopped ${SERVICE}$DEV service..."
}

DEV=$2

SERVICE="teamd"
DEBUGLOG="/tmp/teamd-debug$DEV.log"
NAMESPACE_PREFIX="asic"
if [ "$DEV" ]; then
    NET_NS="$NAMESPACE_PREFIX$DEV" #name of the network namespace
    SONIC_DB_CLI="sonic-db-cli -n $NET_NS"
else
    SONIC_DB_CLI="sonic-db-cli"
fi

case "$1" in
    start|wait|stop)
        $1
        ;;
    *)
        echo "Usage: $0 {start|wait|stop}"
        exit 1
        ;;
esac
