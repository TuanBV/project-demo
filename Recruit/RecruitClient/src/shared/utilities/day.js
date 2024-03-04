import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import weekday from 'dayjs/plugin/weekday';
import dayOfYear from 'dayjs/plugin/dayOfYear';
import customParseFormat from 'dayjs/plugin/customParseFormat';

dayjs.extend(dayOfYear);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(weekday);

dayjs.extend(customParseFormat);
dayjs.getDateUnix = (value = dayjs().unix(), timeZone = 'Asia/Ho_Chi_Minh') => (dayjs.unix(value).tz(timeZone));
dayjs.getDate = (value = dayjs(), timeZone = 'Asia/Ho_Chi_Minh') => (dayjs.tz(value, timeZone));
dayjs.getDateNoTimezone = (value = dayjs()) => (dayjs(value));

export default dayjs;
