import { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import { parseCSV } from '../utils/csvParser';

export function useCharacterData() {
  const { setData, setLoading, setError } = useAppStore();

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const data = await parseCSV('/Just Characters-Table 1.csv');
        setData(data);
      } catch (error) {
        console.error('Error loading CSV:', error);
        setError(error instanceof Error ? error.message : 'Failed to load data');
      }
    }

    loadData();
  }, [setData, setLoading, setError]);
}
