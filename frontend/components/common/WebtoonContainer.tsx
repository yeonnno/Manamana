import Link from 'next/link';

type Props = {
  categoryTitle: string;
  route?: string;
};

export default function webtoonContainer(props: Props) {
  let categoryTitle = props.categoryTitle;
  let routePage = props.route;

  return (
    <div className="flex justify-between rounded-lg bg-BackgroundLightComponent">
      <div className="text-lg font-bold">{categoryTitle}</div>
      {(routePage === 'my-webtoon' || routePage === 'managola' || routePage === 'genre-taste') && (
        <div className="flex items-center">
          <Link
            href={
              routePage === 'my-webtoon'
                ? '/my-webtoon'
                : routePage === 'managola'
                ? '/managola'
                : 'genre-taste'
            }
          >
            <img src="/images/goOtherPage.png" alt="goOtherPage" />
          </Link>
        </div>
      )}
    </div>
  );
}
